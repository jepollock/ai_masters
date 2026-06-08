* README

author: Jason Pollock
email: jason@pollock.ca, pollocjaso@myvuw.ac.nz

* How to install

If you are reading this, it is installed.

* Directory Layout

rt_iot2022/data - the dataset as downloaded
rt_iot2022/input - the dataset extracted and ready for use
rt_iot2022/bin - where the code is placed
rt_iot2022/output - where the CSV files are placed after the run
rt_iot2022/staged_output - where local runs place their output instead of HDFS
ecs_hadoop_env - the ECS cluster Hadoop makefile variables
ecs_spart_env - the ECS cluster Spark makefile variables

* How to run

The makefile supports two execution modes, ecs and local, picked via a ENV environment variable. "ecs" is the default.

The makefile supports local execution on my laptop.  I didn't debug local on the ECS cluster.

The makefile will ensure proper configured access to kerberos, HDFS and Spark before attempting to launch the job.

There are 3 versions of the script:

1. baseline - the default DecisionTree, without any normalisation or a PCA
2. standardized - the data is target encoded and standardized before training a decision tree
3. pca - the data is target encoded, standardized, and a K=10 PCA filter applied before training a decision tree

This is configured to run via makefile. To run a variant: 

$ make submit_rt_iot2022 VARIANT=baseline
$ make submit_rt_iot2022 VARIANT=standardized
$ make submit_rt_iot2022 VARIANT=pca

or optionally

$ make all

The output will be placed in rt_iot2022/output

To clean the files when complete:

$ make clean_rt_iot2022

* Sample Execution

# first, without a kerberos token:

$ make all

make submit_rt_iot2022 VARIANT=standardized
make[1]: Entering directory '/home/pollocjaso/pollocjaso_aiml427_asst3'
Checking Kerberos
No valid kerberos token, run kinit
make[1]: *** [makefile:25: kinit_check] Error 1
make[1]: Leaving directory '/home/pollocjaso/pollocjaso_aiml427_asst3'
make: *** [makefile:100: submit_rt_iot2022_standardized] Error 2


# After a kerberos tgt is obtained::

co246a-1% make all
make submit_rt_iot2022 VARIANT=standardized
make[1]: Entering directory '/home/pollocjaso/pollocjaso_aiml427_asst3'
Checking Kerberos
Checking HDFS
Checking Spark
hdfs dfs -rm rt_iot2022/input/RT_IOT2022.csv
Deleted rt_iot2022/input/RT_IOT2022.csv
hdfs dfs -rm "rt_iot2022/output/*"
Deleted rt_iot2022/output/_SUCCESS
Deleted rt_iot2022/output/part-00000-4673c361-6806-4a1f-9d2a-d68fc950db83-c000.csv
hdfs dfs -rmdir rt_iot2022/input
mkdir -p rt_iot2022/sentinel
hdfs dfs -mkdir -p rt_iot2022/input
touch rt_iot2022/sentinel/hdfs_path_created
Pushing rt_iot2022/input/RT_IOT2022.csv rt_iot2022/sentinel/hdfs_path_created
for i in rt_iot2022/input/RT_IOT2022.csv ; do \
  echo "Removing $i"; \
  hdfs dfs -rm $i; \
done
Removing rt_iot2022/input/RT_IOT2022.csv
rm: `rt_iot2022/input/RT_IOT2022.csv': No such file or directory
make[1]: [makefile:161: rt_iot2022/sentinel/input_pushed] Error 1 (ignored)
for i in rt_iot2022/input/RT_IOT2022.csv ; do \
  echo "Pushing $i"; \
  hdfs dfs -put $i $i; \
done;
Pushing rt_iot2022/input/RT_IOT2022.csv
touch rt_iot2022/sentinel/input_pushed
echo "Submitting rt_iot2022/bin/rt_iot2022.py"
Submitting rt_iot2022/bin/rt_iot2022.py
hdfs dfs -rm "rt_iot2022/output/*"
rm: `rt_iot2022/output/*': No such file or directory
make[1]: [makefile:173: rt_iot2022/output/rt_iot2022.standardized.output] Error 1 (ignored)
hdfs dfs -rmdir rt_iot2022/output
mkdir -p rt_iot2022/output
spark-submit --name rt_iot2022 \
  --master yarn \
  --deploy-mode cluster \
  --conf spark.yarn.appMasterEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
  --conf spark.executorEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
  rt_iot2022/bin/rt_iot2022.py \
  standardized \
  1 \
  rt_iot2022/input/RT_IOT2022.csv \
  rt_iot2022/output 2>&1
WARNING: Using incubator modules: jdk.incubator.vector
[...] logs removed
26/06/09 11:01:31 INFO Client: Application report for application_1779246655912_1543 (state: FINISHED)
26/06/09 11:01:31 INFO Client: 
	 client token: Token { kind: YARN_CLIENT_TOKEN, service:  }
	 diagnostics: N/A
	 ApplicationMaster host: co246a-6.ecs.vuw.ac.nz
	 ApplicationMaster RPC port: 45171
	 queue: root.default
	 start time: 1780959472822
	 final status: SUCCEEDED
	 tracking URL: https://co246a-9.ecs.vuw.ac.nz:8089/proxy/application_1779246655912_1543/
	 user: pollocjaso
hdfs dfs -get "rt_iot2022/output/*" rt_iot2022/output
rm rt_iot2022/output/_*
touch rt_iot2022/output/rt_iot2022.standardized.output
make[1]: Leaving directory '/home/pollocjaso/pollocjaso_aiml427_asst3'
make submit_rt_iot2022 VARIANT=pca
make[1]: Entering directory '/home/pollocjaso/pollocjaso_aiml427_asst3'
Checking Kerberos
Checking HDFS
Checking Spark
echo "Submitting rt_iot2022/bin/rt_iot2022.py"
Submitting rt_iot2022/bin/rt_iot2022.py
hdfs dfs -rm "rt_iot2022/output/*"
Deleted rt_iot2022/output/_SUCCESS
Deleted rt_iot2022/output/part-00000-6cfa29c7-d92f-44ac-a900-0d28457cfac8-c000.csv
Deleted rt_iot2022/output/part-00000-bd0868ad-8615-429c-a7c7-d012d46edd93-c000.csv
hdfs dfs -rmdir rt_iot2022/output
mkdir -p rt_iot2022/output
spark-submit --name rt_iot2022 \
  --master yarn \
  --deploy-mode cluster \
  --conf spark.yarn.appMasterEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
  --conf spark.executorEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
  rt_iot2022/bin/rt_iot2022.py \
  pca \
  1 \
  rt_iot2022/input/RT_IOT2022.csv \
  rt_iot2022/output 2>&1
WARNING: Using incubator modules: jdk.incubator.vector
[...] logs removed
26/06/09 11:05:32 INFO Client: Application report for application_1779246655912_1544 (state: FINISHED)
26/06/09 11:05:32 INFO Client: 
	 client token: N/A
	 diagnostics: N/A
	 ApplicationMaster host: co246a-3.ecs.vuw.ac.nz
	 ApplicationMaster RPC port: 39569
	 queue: root.default
	 start time: 1780959703647
	 final status: SUCCEEDED
	 tracking URL: https://co246a-9.ecs.vuw.ac.nz:8089/proxy/application_1779246655912_1544/
	 user: pollocjaso
hdfs dfs -get "rt_iot2022/output/*" rt_iot2022/output
rm rt_iot2022/output/_*
touch rt_iot2022/output/rt_iot2022.pca.output
make[1]: Leaving directory '/home/pollocjaso/pollocjaso_aiml427_asst3'
make submit_rt_iot2022 VARIANT=baseline
make[1]: Entering directory '/home/pollocjaso/pollocjaso_aiml427_asst3'
Checking Kerberos
Checking HDFS
Checking Spark
echo "Submitting rt_iot2022/bin/rt_iot2022.py"
Submitting rt_iot2022/bin/rt_iot2022.py
hdfs dfs -rm "rt_iot2022/output/*"
Deleted rt_iot2022/output/_SUCCESS
Deleted rt_iot2022/output/part-00000-8e40ed32-b3ec-4f72-aa1d-9e330d49bb6e-c000.csv
Deleted rt_iot2022/output/part-00000-cef24cc0-6184-464c-8ff2-82d3977f1cbf-c000.csv
hdfs dfs -rmdir rt_iot2022/output
mkdir -p rt_iot2022/output
spark-submit --name rt_iot2022 \
  --master yarn \
  --deploy-mode cluster \
  --conf spark.yarn.appMasterEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
  --conf spark.executorEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
  rt_iot2022/bin/rt_iot2022.py \
  baseline \
  1 \
  rt_iot2022/input/RT_IOT2022.csv \
  rt_iot2022/output 2>&1
WARNING: Using incubator modules: jdk.incubator.vector
[...] logs removed
26/06/09 11:06:33 INFO Client: Application report for application_1779246655912_1545 (state: FINISHED)
26/06/09 11:06:33 INFO Client: 
	 client token: N/A
	 diagnostics: N/A
	 ApplicationMaster host: co246a-5.ecs.vuw.ac.nz
	 ApplicationMaster RPC port: 45149
	 queue: root.default
	 start time: 1780959945239
	 final status: SUCCEEDED
	 tracking URL: https://co246a-9.ecs.vuw.ac.nz:8089/proxy/application_1779246655912_1545/
	 user: pollocjaso
hdfs dfs -get "rt_iot2022/output/*" rt_iot2022/output
rm rt_iot2022/output/_*
touch rt_iot2022/output/rt_iot2022.baseline.output

$ cat rt_iot2022/output/*

variant,dataset,average_accuracy,stddev
baseline,test,0.9529405393696523,0.0
baseline,train,0.9527295933167025,0.0
variant,label,precision_mean,recall_mean
standardized,Wipro_bulb,0.5163934426229508,0.9
standardized,NMAP_XMAS_TREE_SCAN,0.0,0.0
[...]

$ make clean_rt_iot2022
Checking Kerberos
Checking HDFS
Checking Spark
hdfs dfs -rm rt_iot2022/input/RT_IOT2022.csv
Deleted rt_iot2022/input/RT_IOT2022.csv
hdfs dfs -rm "rt_iot2022/output/*"
Deleted rt_iot2022/output/_SUCCESS
Deleted rt_iot2022/output/part-00000-3375c992-7f2d-47a5-bb59-d20152be7b5a-c000.csv
Deleted rt_iot2022/output/part-00000-7d064485-9649-4e70-8652-3c454ab0594f-c000.csv
hdfs dfs -rmdir rt_iot2022/input
hdfs dfs -rmdir "rt_iot2022/output"
hdfs dfs -rmdir "rt_iot2022"
rm rt_iot2022/sentinel/hdfs_path_created rt_iot2022/sentinel/input_pushed
rm rt_iot2022/output/*
rm rt_iot2022/output/.*
rm: cannot remove 'rt_iot2022/output/.*': No such file or directory
make: [makefile:122: clean_rt_iot2022] Error 1 (ignored)
rmdir rt_iot2022/output
rm rt_iot2022/staged_output/*
rm: cannot remove 'rt_iot2022/staged_output/*': No such file or directory
make: [makefile:124: clean_rt_iot2022] Error 1 (ignored)
rm rt_iot2022/staged_output/.*
rm: cannot remove 'rt_iot2022/staged_output/.*': No such file or directory
make: [makefile:125: clean_rt_iot2022] Error 1 (ignored)
rmdir rt_iot2022/staged_output
rmdir: failed to remove 'rt_iot2022/staged_output': No such file or directory
make: [makefile:126: clean_rt_iot2022] Error 1 (ignored)

