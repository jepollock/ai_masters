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

make submit_rt_iot2022 VARIANT=standardized
make[1]: Entering directory '/home/pollocjaso/pollocjaso_aiml427_asst3'
Checking Kerberos
Checking HDFS
Checking Spark
echo "Submitting rt_iot2022/bin/rt_iot2022.py"
Submitting rt_iot2022/bin/rt_iot2022.py
hdfs dfs -rm "rt_iot2022/output/*"
Deleted rt_iot2022/output/_SUCCESS
Deleted rt_iot2022/output/part-00000-1c9cd98e-962c-4642-a5f9-372540c92944-c000.csv
hdfs dfs -rmdir rt_iot2022/output
mkdir -p rt_iot2022/output
spark-submit --name rt_iot2022 \
          --driver-memory 7g \
  --master yarn \
  --deploy-mode cluster \
  --conf spark.yarn.appMasterEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
  --conf spark.executorEnv.JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
  rt_iot2022/bin/rt_iot2022.py \
  standardized \
  10 \
  rt_iot2022/input/RT_IOT2022.csv \
  rt_iot2022/output 2>&1
[...] logs removed
DecisionTreeClassificationModel: uid=DecisionTreeClassifier_fe0870c16642, depth=5, numNodes=27, numClasses=13, numFeatures=83
  If (feature 1 <= 21.5)
   If (feature 27 <= 117.5)
    If (feature 82 in {1.0})
     Predict: 4.0
    Else (feature 82 not in {1.0})
     If (feature 17 <= 0.5)
      If (feature 82 in {0.0})
       Predict: 5.0
      Else (feature 82 not in {0.0})
       Predict: 1.0
     Else (feature 17 > 0.5)
      Predict: 6.0
   Else (feature 27 > 117.5)
    Predict: 0.0
[...] logs removed
