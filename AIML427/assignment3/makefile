
# Environment variable loading and exporting.
ENV?=ecs


.PHONY: kinit_check env_check clean

# Environment checks to ensure values are populated and working.
env_check:
	echo $(HADOOP_HOME)
	echo $(PATH)
	echo $$HADOOP_CONF_DIR

kinit_check:
	@echo "Checking Kerberos"
	@if [ "$(ENV)" != "ecs" ]; then \
		echo "Skipping ECS only steps..."; \
		exit 0; \
	fi; \
	klist -s || (echo "No valid kerberos token, run kinit" && exit 1)

hdfs_check:
	@echo "Checking HDFS"
	@if [ "$(ENV)" != "ecs" ]; then \
		echo "Skipping ECS only steps..."; \
		exit 0; \
	fi; \
	hdfs dfs -ls / >/dev/null || (echo "Unable to connect to hdfs" && exit 1)

spark_check:
	@echo "Checking Spark"
	@if [ "$(ENV)" != "ecs" ]; then \
		echo "Skipping ECS only steps..."; \
		exit 0; \
	fi ; \
	echo 'val data = spark.range(1, 1000); data.count()' | spark-shell >/dev/null 2>&1 || (echo "Unable to connect to Spark" && exit 1)

# Each script has it's own tree.
# ScriptName/input
# ScriptName/output
# ScriptName/bin
# ScriptName/sentinel
#
# input goes in the input directory
# output will be placed in the output directory
# bin is where the script goes.
# sentinel are where timestamped files are placed in an
# attempt to keep HDFS in sync.

# To use this, take a copy change "SCRIPT" to the script you're adding
# and change the name in _NAME.
#
# To use:
# make clean_SparkWordCount - clean out the HDFS tree and the local sentinels
# make submit_SparkWordCount - prepare HDFS, submit the job and copy the output back
#
# make local_SparkWordCount ENV=local - run the script locally.

SCRIPT_NAME=rt_iot2022
SCRIPT_BIN_DIR=$(SCRIPT_NAME)/bin
SCRIPT_INPUT_DIR=$(SCRIPT_NAME)/input
SCRIPT_OUTPUT_DIR=$(SCRIPT_NAME)/output
SCRIPT_SENTINEL_DIR=$(SCRIPT_NAME)/sentinel

SCRIPT_EXEC=$(SCRIPT_BIN_DIR)/$(SCRIPT_NAME).py
SCRIPT_INPUT=$(wildcard $(SCRIPT_INPUT_DIR)/*)
SCRIPT_OUTPUT=$(SCRIPT_OUTPUT_DIR)/$(SCRIPT_NAME).output

SCRIPT_HDFS_SENTINEL=$(SCRIPT_SENTINEL_DIR)/hdfs_path_created
SCRIPT_PUSH_SENTINEL=$(SCRIPT_SENTINEL_DIR)/input_pushed
SCRIPT_SENTINELS=$(SCRIPT_HDFS_SENTINEL) $(SCRIPT_PUSH_SENTINEL)
SCRIPT_CHECK=$(SCRIPT_NAME)_check

SCRIPT_NUM_RUNS=1

$(SCRIPT_CHECK): | kinit_check hdfs_check spark_check

clean_$(SCRIPT_NAME): | $(SCRIPT_CHECK)
	-hdfs dfs -rm $(SCRIPT_INPUT)
	-hdfs dfs -rm "$(SCRIPT_OUTPUT_DIR)/*"
	-hdfs dfs -rmdir $(SCRIPT_INPUT_DIR)
	-hdfs dfs -rmdir "$(SCRIPT_OUTPUT_DIR)"
	-hdfs dfs -rmdir "$(SCRIPT_NAME)"
	-rm $(SCRIPT_SENTINELS)
	-rm $(SCRIPT_OUTPUT_DIR)/*
	-rm $(SCRIPT_OUTPUT_DIR)/.*
	-rmdir $(SCRIPT_OUTPUT_DIR)
	-rm $(SCRIPT_STAGED_OUTPUT_DIR)/*
	-rm $(SCRIPT_STAGED_OUTPUT_DIR)/.*
	-rmdir $(SCRIPT_STAGED_OUTPUT_DIR)

submit_$(SCRIPT_NAME): $(SCRIPT_OUTPUT)


SCRIPT_STAGED_OUTPUT_DIR=$(SCRIPT_NAME)/staged_output
local_$(SCRIPT_NAME):
	echo "LOCAL - Submitting $(SCRIPT_EXEC)"
	-rm $(SCRIPT_STAGED_OUTPUT_DIR)/*
	-rm $(SCRIPT_STAGED_OUTPUT_DIR)/.*
	-rmdir $(SCRIPT_STAGED_OUTPUT_DIR)
	-mkdir -p $(SCRIPT_OUTPUT_DIR)
	spark-submit --name $(SCRIPT_NAME) \
	  --master "local[*]"  \
	  $(SCRIPT_EXEC) \
	  $(SCRIPT_NUM_RUNS) \
	  $(SCRIPT_INPUT) \
	  $(SCRIPT_STAGED_OUTPUT_DIR) 2>&1
	cp $(SCRIPT_STAGED_OUTPUT_DIR)/* $(SCRIPT_OUTPUT_DIR)
	touch $(SCRIPT_OUTPUT)

$(SCRIPT_HDFS_SENTINEL): | $(SCRIPT_CHECK)
	-hdfs dfs -rm $(SCRIPT_INPUT)
	-hdfs dfs -rm "$(SCRIPT_OUTPUT_DIR)/*"
	-hdfs dfs -rmdir $(SCRIPT_INPUT_DIR)
	-mkdir -p $(SCRIPT_SENTINEL_DIR)
	hdfs dfs -mkdir -p $(SCRIPT_INPUT_DIR)
	touch $(SCRIPT_HDFS_SENTINEL)

$(SCRIPT_PUSH_SENTINEL): $(SCRIPT_INPUT) $(SCRIPT_HDFS_SENTINEL) | $(SCRIPT_CHECK)
	@echo "Pushing $?"
	-for i in $(filter-out $(SCRIPT_SENTINEL_DIR)/%, $?) ; do \
	  echo "Removing $$i"; \
	  hdfs dfs -rm $$i; \
	done
	for i in $(filter-out $(SCRIPT_SENTINEL_DIR)/%, $?) ; do \
	  echo "Pushing $$i"; \
	  hdfs dfs -put $$i $$i; \
	done;
	touch $(SCRIPT_PUSH_SENTINEL)

$(SCRIPT_OUTPUT): $(SCRIPT_HDFS_SENTINEL) $(SCRIPT_PUSH_SENTINEL) $(SCRIPT_EXEC) | $(SCRIPT_CHECK)
	echo "Submitting $(SCRIPT_EXEC)"
	-hdfs dfs -rm "$(SCRIPT_OUTPUT_DIR)/*"
	-hdfs dfs -rmdir $(SCRIPT_OUTPUT_DIR)
	-mkdir -p $(SCRIPT_OUTPUT_DIR)
	spark-submit --name $(SCRIPT_NAME) \
	  --master yarn \
	  --deploy-mode cluster \
	  --conf spark.yarn.appMasterEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
	  --conf spark.executorEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
	  $(SCRIPT_EXEC) \
	  $(SCRIPT_NUM_RUNS) \
	  $(SCRIPT_INPUT) \
	  $(SCRIPT_OUTPUT_DIR) 2>&1
	-rm $(SCRIPT_OUTPUT_DIR)/*
	hdfs dfs -get "$(SCRIPT_OUTPUT_DIR)/*" $(SCRIPT_OUTPUT_DIR)
	touch $(SCRIPT_OUTPUT)



NORMAL_NAME=rt_iot2022_normal
NORMAL_BIN_DIR=$(NORMAL_NAME)/bin
NORMAL_INPUT_DIR=$(NORMAL_NAME)/input
NORMAL_OUTPUT_DIR=$(NORMAL_NAME)/output
NORMAL_SENTINEL_DIR=$(NORMAL_NAME)/sentinel

NORMAL_EXEC=$(NORMAL_BIN_DIR)/$(NORMAL_NAME).py
NORMAL_INPUT=$(wildcard $(NORMAL_INPUT_DIR)/*)
NORMAL_OUTPUT=$(NORMAL_OUTPUT_DIR)/$(NORMAL_NAME).output

NORMAL_HDFS_SENTINEL=$(NORMAL_SENTINEL_DIR)/hdfs_path_created
NORMAL_PUSH_SENTINEL=$(NORMAL_SENTINEL_DIR)/input_pushed
NORMAL_SENTINELS=$(NORMAL_HDFS_SENTINEL) $(NORMAL_PUSH_SENTINEL)
NORMAL_CHECK=$(NORMAL_NAME)_check

NORMAL_NUM_RUNS=1

$(NORMAL_CHECK): | kinit_check hdfs_check spark_check

clean_$(NORMAL_NAME): | $(NORMAL_CHECK)
	-hdfs dfs -rm $(NORMAL_INPUT)
	-hdfs dfs -rm "$(NORMAL_OUTPUT_DIR)/*"
	-hdfs dfs -rmdir $(NORMAL_INPUT_DIR)
	-hdfs dfs -rmdir "$(NORMAL_OUTPUT_DIR)"
	-hdfs dfs -rmdir "$(NORMAL_NAME)"
	-rm $(NORMAL_SENTINELS)
	-rm $(NORMAL_OUTPUT_DIR)/*
	-rm $(NORMAL_OUTPUT_DIR)/.*
	-rmdir $(NORMAL_OUTPUT_DIR)
	-rm $(NORMAL_STAGED_OUTPUT_DIR)/*
	-rm $(NORMAL_STAGED_OUTPUT_DIR)/.*
	-rmdir $(NORMAL_STAGED_OUTPUT_DIR)

submit_$(NORMAL_NAME): $(NORMAL_OUTPUT)


NORMAL_STAGED_OUTPUT_DIR=$(NORMAL_NAME)/staged_output
local_$(NORMAL_NAME):
	echo "LOCAL - Submitting $(NORMAL_EXEC)"
	-rm $(NORMAL_STAGED_OUTPUT_DIR)/*
	-rm $(NORMAL_STAGED_OUTPUT_DIR)/.*
	-mkdir -p $(NORMAL_OUTPUT_DIR)
	-rmdir $(NORMAL_STAGED_OUTPUT_DIR)
	spark-submit --name $(NORMAL_NAME) \
	  --master "local[*]"  \
	  $(NORMAL_EXEC) \
	  $(NORMAL_NUM_RUNS) \
	  $(NORMAL_INPUT) \
	  $(NORMAL_STAGED_OUTPUT_DIR) 2>&1
	cp $(NORMAL_STAGED_OUTPUT_DIR)/* $(NORMAL_OUTPUT_DIR)
	touch $(NORMAL_OUTPUT)

$(NORMAL_HDFS_SENTINEL): | $(NORMAL_CHECK)
	-hdfs dfs -rm $(NORMAL_INPUT)
	-hdfs dfs -rm "$(NORMAL_OUTPUT_DIR)/*"
	-hdfs dfs -rmdir $(NORMAL_INPUT_DIR)
	-mkdir -p $(NORMAL_SENTINEL_DIR)
	hdfs dfs -mkdir -p $(NORMAL_INPUT_DIR)
	touch $(NORMAL_HDFS_SENTINEL)

$(NORMAL_PUSH_SENTINEL): $(NORMAL_INPUT) $(NORMAL_HDFS_SENTINEL) | $(NORMAL_CHECK)
	@echo "Pushing $?"
	-for i in $(filter-out $(NORMAL_SENTINEL_DIR)/%, $?) ; do \
	  echo "Removing $$i"; \
	  hdfs dfs -rm $$i; \
	done
	for i in $(filter-out $(NORMAL_SENTINEL_DIR)/%, $?) ; do \
	  echo "Pushing $$i"; \
	  hdfs dfs -put $$i $$i; \
	done;
	touch $(NORMAL_PUSH_SENTINEL)

$(NORMAL_OUTPUT): $(NORMAL_HDFS_SENTINEL) $(NORMAL_PUSH_SENTINEL) $(NORMAL_EXEC) | $(NORMAL_CHECK)
	echo "Submitting $(NORMAL_EXEC)"
	-hdfs dfs -rm "$(NORMAL_OUTPUT_DIR)/*"
	-hdfs dfs -rmdir $(NORMAL_OUTPUT_DIR)
	-mkdir -p $(NORMAL_OUTPUT_DIR)
	spark-submit --name $(NORMAL_NAME) \
	  --master yarn \
	  --deploy-mode cluster \
	  --conf spark.yarn.appMasterEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
	  --conf spark.executorEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
	  $(NORMAL_EXEC) \
	  $(NORMAL_NUM_RUNS) \
	  $(NORMAL_INPUT) \
	  $(NORMAL_OUTPUT_DIR) 2>&1
	-rm $(NORMAL_OUTPUT_DIR)/*
	hdfs dfs -get "$(NORMAL_OUTPUT_DIR)/*" $(NORMAL_OUTPUT_DIR)
	touch $(NORMAL_OUTPUT)


PCA_NAME=rt_iot2022_pca
PCA_BIN_DIR=$(PCA_NAME)/bin
PCA_INPUT_DIR=$(PCA_NAME)/input
PCA_OUTPUT_DIR=$(PCA_NAME)/output
PCA_SENTINEL_DIR=$(PCA_NAME)/sentinel

PCA_EXEC=$(PCA_BIN_DIR)/$(PCA_NAME).py
PCA_INPUT=$(wildcard $(PCA_INPUT_DIR)/*)
PCA_OUTPUT=$(PCA_OUTPUT_DIR)/$(PCA_NAME).output

PCA_HDFS_SENTINEL=$(PCA_SENTINEL_DIR)/hdfs_path_created
PCA_PUSH_SENTINEL=$(PCA_SENTINEL_DIR)/input_pushed
PCA_SENTINELS=$(PCA_HDFS_SENTINEL) $(PCA_PUSH_SENTINEL)
PCA_CHECK=$(PCA_NAME)_check

PCA_NUM_RUNS=1

$(PCA_CHECK): | kinit_check hdfs_check spark_check

clean_$(PCA_NAME): | $(PCA_CHECK)
	-hdfs dfs -rm $(PCA_INPUT)
	-hdfs dfs -rm "$(PCA_OUTPUT_DIR)/*"
	-hdfs dfs -rmdir $(PCA_INPUT_DIR)
	-hdfs dfs -rmdir "$(PCA_OUTPUT_DIR)"
	-hdfs dfs -rmdir "$(PCA_NAME)"
	-rm $(PCA_SENTINELS)
	-rm $(PCA_OUTPUT_DIR)/*
	-rm $(PCA_OUTPUT_DIR)/.*
	-rmdir $(PCA_OUTPUT_DIR)
	-rm $(PCA_STAGED_OUTPUT_DIR)/*
	-rm $(PCA_STAGED_OUTPUT_DIR)/.*
	-rmdir $(PCA_STAGED_OUTPUT_DIR)

submit_$(PCA_NAME): $(PCA_OUTPUT)


PCA_STAGED_OUTPUT_DIR=$(PCA_NAME)/staged_output
local_$(PCA_NAME):
	echo "LOCAL - Submitting $(PCA_EXEC)"
	-rm $(PCA_STAGED_OUTPUT_DIR)/*
	-rm $(PCA_STAGED_OUTPUT_DIR)/.*
	-rmdir $(PCA_STAGED_OUTPUT_DIR)
	-mkdir -p $(PCA_OUTPUT_DIR)
	spark-submit --name $(PCA_NAME) \
	  --master "local[*]"  \
	  $(PCA_EXEC) \
	  $(PCA_NUM_RUNS) \
	  $(PCA_INPUT) \
	  $(PCA_STAGED_OUTPUT_DIR) 2>&1
	cp $(PCA_STAGED_OUTPUT_DIR)/* $(PCA_OUTPUT_DIR)
	touch $(PCA_OUTPUT)

$(PCA_HDFS_SENTINEL): | $(PCA_CHECK)
	-hdfs dfs -rm $(PCA_INPUT)
	-hdfs dfs -rm "$(PCA_OUTPUT_DIR)/*"
	-hdfs dfs -rmdir $(PCA_INPUT_DIR)
	-mkdir -p $(PCA_SENTINEL_DIR)
	hdfs dfs -mkdir -p $(PCA_INPUT_DIR)
	touch $(PCA_HDFS_SENTINEL)

$(PCA_PUSH_SENTINEL): $(PCA_INPUT) $(PCA_HDFS_SENTINEL) | $(PCA_CHECK)
	@echo "Pushing $?"
	-for i in $(filter-out $(PCA_SENTINEL_DIR)/%, $?) ; do \
	  echo "Removing $$i"; \
	  hdfs dfs -rm $$i; \
	done
	for i in $(filter-out $(PCA_SENTINEL_DIR)/%, $?) ; do \
	  echo "Pushing $$i"; \
	  hdfs dfs -put $$i $$i; \
	done;
	touch $(PCA_PUSH_SENTINEL)

$(PCA_OUTPUT): $(PCA_HDFS_SENTINEL) $(PCA_PUSH_SENTINEL) $(PCA_EXEC) | $(PCA_CHECK)
	echo "Submitting $(PCA_EXEC)"
	-hdfs dfs -rm "$(PCA_OUTPUT_DIR)/*"
	-hdfs dfs -rmdir $(PCA_OUTPUT_DIR)
	-mkdir -p $(PCA_OUTPUT_DIR)
	spark-submit --name $(PCA_NAME) \
	  --master yarn \
	  --deploy-mode cluster \
	  --conf spark.yarn.appMasterEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
	  --conf spark.executorEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
	  $(PCA_EXEC) \
	  $(PCA_NUM_RUNS) \
	  $(PCA_INPUT) \
	  $(PCA_OUTPUT_DIR) 2>&1
	-rm $(PCA_OUTPUT_DIR)/*
	hdfs dfs -get "$(PCA_OUTPUT_DIR)/*" $(PCA_OUTPUT_DIR)
	touch $(PCA_OUTPUT)




include $(ENV)_hadoop_env
export $(shell sed 's/=.*//' $(ENV)_hadoop_env)

include $(ENV)_spark_env
export $(shell sed 's/=.*//' $(ENV)_spark_env)

