
# Has to be set so that we can run hadoop
export JAVA_HOME=/usr/lib/jvm/java-7-oracle

# This removes this output directory created by a previous mapreduce job
rm -rf mapreduce/output

./bin/hadoop `#This is the mapreduce executable` \
  jar ./share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar `#Some configurations for the hadoop job` \
  -D mapreduce.job.maps=4 `#Specifies the number of mappers to be 4 for this job` \
  -D mapreduce.job.reduces=2 `#Specifies the number of reducers to be 2 for this job` \
  -input ./mapreduce/sampleInput `#Specifies the input directory` \
  -output ./mapreduce/output `#Creates the output directory for the mapreduce job` \
  -mapper ./mapreduce/map.py `#Specifes the mapper executable` \
  -reducer ./mapreduce/reduce.py `#Specifies the reducer executable`

# The following is an example of how to execute multiple mapreduce jobs in a 'pipeline' fashion
#rm -rf mapreduce/out1

#./bin/hadoop \
  #jar ./share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
  #-D mapreduce.job.maps=30 \
  #-D mapreduce.job.reduces=30 \
  #-input ./mapreduce/input \
  #-output ./mapreduce/out1 \
  #-mapper ./mapreduce/map1.py \
  #-reducer ./mapreduce/reduce1.py \
  #-file ./total_document_count.txt # NOTE: This is how you make a file accessable to mapreduce jobs

#rm -rf mapreduce/out2

#./bin/hadoop \
  #jar ./share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
  #-D mapreduce.job.maps=30 \
  #-D mapreduce.job.reduces=30 \
  #-input ./mapreduce/out1 \
  #-output ./mapreduce/out2 \
  #-mapper ./mapreduce/map2.py \
  #-reducer ./mapreduce/reduce2.py
  #-file ./total_document_count.txt # NOTE: This is how you make a file accessable to mapreduce jobs
