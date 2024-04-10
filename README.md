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