import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

bootstrapServers = sys.argv[1]
subscribeType = sys.argv[2]
topics = sys.argv[3]
output = str(sys.argv[4])

spark = SparkSession\
        .builder\
        .appName("StructuredKafkaWordCount")\
        .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

lines = spark\
        .readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", bootstrapServers)\
        .option(subscribeType, topics)\
        .option("failOnDataLoss", "false")\
        .load()\
        .selectExpr("CAST(value AS STRING)")

words = lines.select(explode(split(lines.value, ' ')).alias('word'))

wordCounts = words.groupBy('word').count().orderBy('count',ascending = False)

query = wordCounts\
	.selectExpr("CAST(word AS STRING) AS key, CAST(count AS STRING) AS value")\
        .writeStream\
        .outputMode('complete')\
        .format('kafka')\
	.option("kafka.bootstrap.servers", bootstrapServers)\
	.option("topic", output)\
        .option("checkpointLocation", "/home/sxr220188/Ubuntu/Programs/checkpoint")\
	.start()\
	.awaitTermination()