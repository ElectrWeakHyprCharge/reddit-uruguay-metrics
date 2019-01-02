import json
from datetime import datetime, timedelta

import requests


SUBMISSIONS = 'submission'
COMMENTS = 'comment'


def pushshift(endpoint, **kwargs):
    return json.loads(requests.get(
        f'https://api.pushshift.io/reddit/{endpoint}/search',
        params=kwargs).text)['data']


def amount_of(endpoint, before, after, sub='all'):
    return pushshift(
        endpoint = endpoint,
        limit = 1000,
        sort_type = 'created_utc',
        sort = 'asc',
        after = int(after.timestamp()),
        before = int(before.timestamp()),
        subreddit = sub
    )


def first_day_of_sub(sub):
    return datetime.utcfromtimestamp(pushshift(
        endpoint=SUBMISSIONS, subreddit=sub, limit=1, sort='asc',
    )[0]['created_utc']).replace(hour=0, minute=0, second=0, microsecond=0)


def all_posts_per_day_from(sub, since=None, until=datetime.now()):
    this_day = since or first_day_of_sub(sub)

    while this_day <= until:
        next_day = this_day + timedelta(days = 1)
        yield (this_day,
            amount_of(SUBMISSIONS, after=this_day, before=next_day, sub=sub),
            amount_of(COMMENTS, after=this_day, before=next_day, sub=sub)
        )
        this_day = next_day



if __name__ == '__main__':
    with open('activity', 'a') as f:
        for day, submissions, comments in all_posts_per_day_from('uruguay', since=datetime(2018,12,21)):
            f.write(f'{day} | {len(submissions)} | {len(comments)}\n')
