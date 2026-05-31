#!/usr/bin/env python3
import logging
import sys

import numpy
import pyspark.sql.functions as F
from pyspark.logger import PySparkLogger
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import IndexToString, StringIndexer, VectorAssembler, TargetEncoder, StandardScaler, \
    OneHotEncoder
from pyspark.ml import Pipeline, Transformer, Estimator, Model
from pyspark.ml.param.shared import HasInputCols, HasOutputCol
from pyspark.ml.util import DefaultParamsWritable
from pyspark.sql import SparkSession, Window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, LongType

PREDICTION_COLUMN = "prediction"
FEATURE_VECTOR_COLUMN = "features"
SCALED_FEATURE_VECTOR_COLUMN = "features_scaled"
LABEL_COLUMN = "label"

# https://xkcd.com/221/ - 4 is overused
RANDOM_SEED = 221

enable_debug = True
def debug(value):
    if enable_debug:
        print(f"JASON: {value}")

def replaceWithSuffix(column_list, to_replace, suffix):
    columns_to_replace = set(to_replace)
    new_names = [x + "_" + suffix for x in columns_to_replace]
    column_list = [item for item in column_list if item not in columns_to_replace]
    column_list.extend(new_names)
    return column_list

class LikelihoodModel(Model, HasInputCols, HasOutputCol, DefaultParamsWritable):
    def __init__(self, inputCols=None, outputCol=None, likelihood_lookup=None):
        super(LikelihoodModel, self).__init__()
        if len(inputCols) != 2:
            raise ValueError("inputCols must contain exactly two columns - {encoded, target}")
        self.likelihood_lookup = likelihood_lookup
        self._set(inputCols=inputCols)
        self._set(outputCol=outputCol)

    def _transform(self, dataset):
        input = self.getInputCols()
        output_col = self.getOutputCol()
        groupby_col = input[0]
        target_col = input[1]

        return dataset.join(
            F.broadcast(self.likelihood_lookup),
            on=[groupby_col, target_col],
            how="left").na.fill({output_col: 0.0}) # Treat new values as not being possible.

class LikelihoodEncoder(Estimator, HasInputCols, HasOutputCol):
    def __init__(self, inputCols=None, outputCol=None):
        super(LikelihoodEncoder, self).__init__()
        # Assert the values are set as early as possible.
        if len(inputCols) != 2:
            raise ValueError("inputCols must contain exactly two columns - {encoded, target}")
        self._set(inputCols=inputCols)
        self._set(outputCol=outputCol)

    def _fit(self, dataset):
        input = self.getInputCols()
        output_col = self.getOutputCol()
        groupby_col = input[0]
        target_col = input[1]

        groupby_window = Window.partitionBy(groupby_col)
        pairwise_window = Window.partitionBy(groupby_col, target_col)

        # at this point, we've got the rows grouped by the group_by
        # we've also got the rows grouped by group_by, target.
        # Update the dataset, creating a new column, matching_count and total_count
        # Then update it again, and calculate the probability.
        count_temp = "_matching_count"
        total_temp = "_total_count"
        count = "count"

        groupby_totals = dataset.groupBy(groupby_col).count().withColumnRenamed(count, total_temp)
        pairwise_totals = dataset.groupby(groupby_col, target_col).count().withColumnRenamed(count, count_temp)

        likelihood_lookup = (pairwise_totals.join(groupby_totals, on=groupby_col)
                             .withColumn(output_col, F.col(count_temp) / F.col(total_temp))
                             .select(groupby_col, target_col, output_col)
                             )
        return LikelihoodModel(inputCols=input, outputCol=output_col, likelihood_lookup=likelihood_lookup)


def main():
    if len(sys.argv) != 4:
        print("Usage: rt_iot2022_normal.py <num_runs> <input_file> <output_dir>")
        sys.exit(-1)

    num_runs = int(sys.argv[1])
    input_path = sys.argv[2]
    output_path = sys.argv[3]

    spark = SparkSession.builder.appName("rt_iot2022_normal").getOrCreate()

    # generated using to_schema.sh
    # Updated 32, 33 to LongType.
    schema = StructType([
        StructField("no", LongType()),
        StructField("id.orig_p", LongType()),
        StructField("id.resp_p", DoubleType()),
        StructField("proto", StringType()),
        StructField("service", StringType()),
        StructField("flow_duration", DoubleType()),
        StructField("fwd_pkts_tot", DoubleType()),
        StructField("bwd_pkts_tot", LongType()),
        StructField("fwd_data_pkts_tot", LongType()),
        StructField("bwd_data_pkts_tot", LongType()),
        StructField("fwd_pkts_per_sec", DoubleType()),
        StructField("bwd_pkts_per_sec", DoubleType()),
        StructField("flow_pkts_per_sec", DoubleType()),
        StructField("down_up_ratio", DoubleType()),
        StructField("fwd_header_size_tot", LongType()),
        StructField("fwd_header_size_min", LongType()),
        StructField("fwd_header_size_max", LongType()),
        StructField("bwd_header_size_tot", LongType()),
        StructField("bwd_header_size_min", LongType()),
        StructField("bwd_header_size_max", LongType()),
        StructField("flow_FIN_flag_count", LongType()),
        StructField("flow_SYN_flag_count", LongType()),
        StructField("flow_RST_flag_count", LongType()),
        StructField("fwd_PSH_flag_count", LongType()),
        StructField("bwd_PSH_flag_count", LongType()),
        StructField("flow_ACK_flag_count", LongType()),
        StructField("fwd_URG_flag_count", LongType()),
        StructField("bwd_URG_flag_count", LongType()),
        StructField("flow_CWR_flag_count", LongType()),
        StructField("flow_ECE_flag_count", LongType()),
        StructField("fwd_pkts_payload.min", DoubleType()),
        StructField("fwd_pkts_payload.max", DoubleType()),
        StructField("fwd_pkts_payload.tot", DoubleType()),
        StructField("fwd_pkts_payload.avg", DoubleType()),
        StructField("fwd_pkts_payload.std", DoubleType()),
        StructField("bwd_pkts_payload.min", DoubleType()),
        StructField("bwd_pkts_payload.max", DoubleType()),
        StructField("bwd_pkts_payload.tot", DoubleType()),
        StructField("bwd_pkts_payload.avg", DoubleType()),
        StructField("bwd_pkts_payload.std", DoubleType()),
        StructField("flow_pkts_payload.min", DoubleType()),
        StructField("flow_pkts_payload.max", DoubleType()),
        StructField("flow_pkts_payload.tot", DoubleType()),
        StructField("flow_pkts_payload.avg", DoubleType()),
        StructField("flow_pkts_payload.std", DoubleType()),
        StructField("fwd_iat.min", DoubleType()),
        StructField("fwd_iat.max", DoubleType()),
        StructField("fwd_iat.tot", DoubleType()),
        StructField("fwd_iat.avg", DoubleType()),
        StructField("fwd_iat.std", DoubleType()),
        StructField("bwd_iat.min", DoubleType()),
        StructField("bwd_iat.max", DoubleType()),
        StructField("bwd_iat.tot", DoubleType()),
        StructField("bwd_iat.avg", DoubleType()),
        StructField("bwd_iat.std", DoubleType()),
        StructField("flow_iat.min", DoubleType()),
        StructField("flow_iat.max", DoubleType()),
        StructField("flow_iat.tot", DoubleType()),
        StructField("flow_iat.avg", DoubleType()),
        StructField("flow_iat.std", DoubleType()),
        StructField("payload_bytes_per_second", DoubleType()),
        StructField("fwd_subflow_pkts", DoubleType()),
        StructField("bwd_subflow_pkts", DoubleType()),
        StructField("fwd_subflow_bytes", DoubleType()),
        StructField("bwd_subflow_bytes", DoubleType()),
        StructField("fwd_bulk_bytes", DoubleType()),
        StructField("bwd_bulk_bytes", DoubleType()),
        StructField("fwd_bulk_packets", DoubleType()),
        StructField("bwd_bulk_packets", DoubleType()),
        StructField("fwd_bulk_rate", DoubleType()),
        StructField("bwd_bulk_rate", DoubleType()),
        StructField("active.min", DoubleType()),
        StructField("active.max", DoubleType()),
        StructField("active.tot", DoubleType()),
        StructField("active.avg", DoubleType()),
        StructField("active.std", DoubleType()),
        StructField("idle.min", DoubleType()),
        StructField("idle.max", DoubleType()),
        StructField("idle.tot", DoubleType()),
        StructField("idle.avg", DoubleType()),
        StructField("idle.std", DoubleType()),
        StructField("fwd_init_window_size", LongType()),
        StructField("bwd_init_window_size", LongType()),
        StructField("fwd_last_window_size", LongType()),
        StructField("Attack_type", StringType())
    ])
    raw_dataframe = spark.read.schema(schema).csv(input_path, header=True)
    # fix column naming to go from . -> _
    for column in raw_dataframe.columns:
        if '.' in column:
            raw_dataframe = raw_dataframe.withColumnRenamed(column, column.replace('.', '_'))
    feature_columns = raw_dataframe.columns
    feature_columns.remove("Attack_type")
    feature_columns.remove("no")


    # ok we need to deal with
    # StructField("id.orig_p", LongType()),
    # StructField("id.resp_p", DoubleType()),
    # StructField("proto", StringType()),
    # StructField("service", StringType()),

    # Ensure defined order, hand translate.
    to_index = ["Attack_type", "proto", "service"]
    indexed = [LABEL_COLUMN, "proto_indexed", "service_indexed"]
    label_indexer = StringIndexer(inputCols=to_index, outputCols=indexed)
    feature_columns = replaceWithSuffix(feature_columns, ["proto", "service"], "indexed")

    # Convert the value based on their probability of the target class being "correct"
    to_target_encode = ["id_orig_p", "id_resp_p", "proto_indexed", "service_indexed"]
    target_encoded = ["id_orig_p_tgt", "id_resp_p_tgt", "proto_indexed_tgt", "service_indexed_tgt"]
    likelihood_encoders = []
    for (source, target) in zip(to_target_encode, target_encoded):
        likelihood_encoders.append(LikelihoodEncoder(inputCols=[source, LABEL_COLUMN], outputCol=target))
    feature_columns = replaceWithSuffix(feature_columns, to_target_encode, "tgt")

    feature_vector_assembler = VectorAssembler(inputCols=feature_columns, outputCol=FEATURE_VECTOR_COLUMN)

    feature_vector_scaler = StandardScaler(inputCol=FEATURE_VECTOR_COLUMN, outputCol=SCALED_FEATURE_VECTOR_COLUMN)

    decision_tree = DecisionTreeClassifier(labelCol=LABEL_COLUMN, featuresCol=SCALED_FEATURE_VECTOR_COLUMN)
    pipeline_stages = []
    pipeline_stages.append(label_indexer)
    pipeline_stages.extend(likelihood_encoders)
    pipeline_stages.extend([feature_vector_assembler, feature_vector_scaler, decision_tree])
    pipeline = Pipeline(stages = pipeline_stages)

    training_data = [None] * num_runs
    test_data = [None] * num_runs
    # Split the data into training and test sets (30% held out for testing)
    # Make sure each split has a different, deterministic seed.
    for i in range(num_runs):
        training_data[i], test_data[i] = raw_dataframe.randomSplit([0.7, 0.3], seed=RANDOM_SEED + i)

    # Train num_runs models
    trained_models = []
    for train in training_data:
        trained_models.append(pipeline.fit(train))

    # Predict the results of the 10 trees.
    predictions = []
    for (model, training, test) in zip(trained_models, training_data, test_data):
        predictions.append([model.transform(training), model.transform(test)])

    # Print some output, just because.
    predictions[0][1].select(LABEL_COLUMN, PREDICTION_COLUMN).show(5)

    # Report the 10 results.
    # remove max(Accuracy), min(accuracy), average(accuracy) std_dev(accuracy)
    # Get the accuracies.
    evaluator = MulticlassClassificationEvaluator(labelCol=LABEL_COLUMN,
                                                  predictionCol=PREDICTION_COLUMN,
                                                  metricName="accuracy")
    accuracies = numpy.empty((0, 2))
    debug(f"predictions.size = {len(predictions)}")
    for (train_prediction, test_prediction) in predictions:
        train_prediction.select(LABEL_COLUMN, PREDICTION_COLUMN).show(5)
        test_prediction.select(LABEL_COLUMN, PREDICTION_COLUMN).show(5)
        accuracies = numpy.append(accuracies, [[evaluator.evaluate(train_prediction), evaluator.evaluate(test_prediction)]], axis=0)

    debug(f"Accuracies.shape = {accuracies.shape}")

    # Python _sometimes_ has type safety. But only _sometimes_
    data = [
        ( "normalized_test", float(numpy.average(accuracies[:, 1])), float(numpy.std(accuracies[:, 1]))),
        ("normalized_train", float(numpy.average(accuracies[:, 0])), float(numpy.std(accuracies[:, 0])))
    ]
    out_schema = StructType([
        StructField("dataset", StringType(), False),
        StructField("average", DoubleType(), False),
        StructField("stddev", DoubleType(), False)
    ])
    output_dataframe = spark.createDataFrame(data, schema=out_schema)

    # output_dataframe = spark.createDataFrame(data, schema=["max", "min", "average", "stddev"])
    output_dataframe.coalesce(1).write.mode("errorifexists").option("header", "true").csv(output_path)

    spark.stop()

if __name__ == "__main__":
    main()


