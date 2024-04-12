import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import explode, split, col, to_json, struct, udf
import spacy

bootstrapServers = sys.argv[1]
subscribeType = sys.argv[2]
topics = sys.argv[3]
output = str(sys.argv[4])

spark = SparkSession\
        .builder\
        .appName("StructuredKafkaWordCount")\
        .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

#loal the spacy model
nlp = spacy.load("en_core_web_sm")

#udf - User Defined Function for dataframe
def ner(raw_text):
    doc = nlp(raw_text)
    entities = [ent.text for ent in doc.ents]
    return ' '.join(entities) if entities else None

ner_udf = udf(ner, StringType())

lines = spark\
        .readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", bootstrapServers)\
        .option(subscribeType, topics)\
        .option("failOnDataLoss", "false")\
        .load()\
        .selectExpr("CAST(value AS STRING)")

words = lines.select(explode(split(ner_udf('value'), ' ')).alias('word'))

wordCounts = words.groupBy('word').count()

query = wordCounts\
        .select(to_json(struct(col("word"), col("count"))).alias("value"))\
        .writeStream\
        .outputMode('update')\
        .format('kafka')\
	.option("kafka.bootstrap.servers", bootstrapServers)\
	.option("topic", output)\
        .option("checkpointLocation", "/home/sxr220188/Ubuntu/Programs/checkpoint")\
	.start()\
	.awaitTermination()
