import sys
import re
import praw
from kafka import KafkaProducer

def clean_comment(comment_body):
    if not comment_body:
        return None  # Skip truly empty comments

    cleaned_comment = comment_body.strip()
    cleaned_comment = re.sub(r'\s+', ' ', cleaned_comment)
    return cleaned_comment.encode('utf-8') if cleaned_comment else None

reddit = praw.Reddit(
    client_id="6d_rhJ4xW1qGyn0TOhd8xQ",
    client_secret="5UksOI6uuA0oOiLL6eDTEDmiqb7kQg",
    user_agent="Python:assignment:1.0 (by /u/FeedApprehensive9296)",
)

producer = KafkaProducer(bootstrap_servers=['172.19.49.193:9092'])  # Encode data as bytes

topic_name = str(sys.argv[1])
subreddit = reddit.subreddit('askReddit')

for comment in subreddit.stream.comments():
    cleaned_message = clean_comment(comment.body)
    if cleaned_message:
        producer.send(topic_name, value=cleaned_message)
