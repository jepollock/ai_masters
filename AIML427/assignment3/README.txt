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

