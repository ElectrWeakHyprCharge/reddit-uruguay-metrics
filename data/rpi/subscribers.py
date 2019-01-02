import praw
from datetime import datetime
import gzip


reddit = praw.Reddit(
            'bot-ija',
            user_agent='Record of the /r/uruguay subscriber count'
)

subscribers = reddit.subreddit('uruguay').subscribers

with gzip.open('subscriber_count', 'at') as f:
    f.write(f'{datetime.utcnow()} | {subscribers}\n')

