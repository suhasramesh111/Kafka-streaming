# Kafka-streaming description  
 This repo helps i getting the realtime wordcount of reddit comments for a specific subreddit using Kafka and spark and also helps visualize it using elastic stack  

### Prerequisites
 This application need the following applications installed:  
 1. Apache Spark  
 2. Kafka  

 You would also need to install the following libraries:  
 1. PRAW (pip install praw)  
 2. kafka-python (pip install kafka-python)  

### Directions to use
 #### Go to your kafka installation folder and run the following commands
 
 1. bin/zookeeper-server-start.sh -daemon config/zookeeper.properties   
 This starts zookeeper in daemon mode  

 2. bin/kafka-server-start.sh -daemon config/server.properties    
 This starts the kafka server  

 3. bin/kafka-console-producer.sh --topic reddit_comments --bootstrap-server localhost:9092     
 This creates a topic in kafka topic called reddit_comments (can be any name). This is where the writter.py will write the comments extracted from reddit.  
 
 bin/kafka-console-producer.sh --topic wordCountOutput --bootstrap-server localhost:9092    
 We will need to create another topic called wordCountOutput (can be any name) to store the output of the wordcount.py file. This is where the actual word count happens.     

 #### Run the python files
 
 1. writer.py
 This file is used to write data onto the kafka topic (In this case, the topic it is writing to is reddit_comments). This file keeps extracting comments from reddit until terminated.   
 It takes 1 argument - kafka topic on which it has to write.   

 Syntax: python3 writer.py <topic_name>    
 Ex: python3 writer.py reddit_comments   

 2. wordcount.py   
 This is to be run with spark-submit. It writes the output onto another kafka file(In this case, the topic it is writing to is wordCountOutput). It runs until termination and calculates a running word count.    
 It requires to be run with the package - org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 (version 3.5.1 is important).   
 It also takes 3 arguments - Bootstrap server(server on which kafka is running), subscribe mode, topic where the comments are being sent, topic where the output has to be written to.   

 Syntax: spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 wordcount.py <bootstrap_server> <subscribe_mode> <topic_1> <topic_2>   
 Ex: spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 wordcount.py localhost:9092 subscribe reddit_comments wordcount   

