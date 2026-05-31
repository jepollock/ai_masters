#!/usr/bin/env python3
import logging
import sys

import numpy
from pyspark.logger import PySparkLogger
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import IndexToString, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, LongType

PREDICTION_COLUMN = "prediction"
FEATURE_VECTOR_COLUMN = "features"
LABEL_COLUMN = "label"

# https://xkcd.com/221/ - 4 is overused
RANDOM_SEED = 221

enable_debug = True
def debug(value):
    if enable_debug:
        print(f"JASON: {value}")

def main():
    if len(sys.argv) != 4:
        print("Usage: rt_iot2022.py <num_runs> <input_file> <output_dir>")
        sys.exit(-1)

    num_runs = int(sys.argv[1])
    input_path = sys.argv[2]
    output_path = sys.argv[3]

    spark = SparkSession.builder.appName("rt_iot2022").getOrCreate()

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

    # we also need to transform proto and service, remove them and replace with the renamed columns.
    feature_columns_to_index = set(["proto", "service"])
    indexed_feature_columns = [ x + "_indexed" for x in feature_columns_to_index]
    feature_columns = [item for item in feature_columns if item not in feature_columns_to_index]
    feature_columns.extend(indexed_feature_columns)

    # Ensure defined order, hand translate.
    to_index = ["Attack_type", "proto", "service"]
    indexed = [LABEL_COLUMN, "proto_indexed", "service_indexed"]
    label_indexer = StringIndexer(inputCols=to_index, outputCols=indexed)

    feature_vector_assembler = VectorAssembler(inputCols=feature_columns, outputCol=FEATURE_VECTOR_COLUMN)

    decision_tree = DecisionTreeClassifier(labelCol=LABEL_COLUMN, featuresCol=FEATURE_VECTOR_COLUMN)
    pipeline = Pipeline(stages = [label_indexer, feature_vector_assembler, decision_tree])

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
        ( "test", float(numpy.average(accuracies[:, 1])), float(numpy.std(accuracies[:, 1]))),
        ("train", float(numpy.average(accuracies[:, 0])), float(numpy.std(accuracies[:, 0])))
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


