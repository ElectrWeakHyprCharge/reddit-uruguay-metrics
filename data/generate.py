from typing import Iterator, Tuple, Union
from itertools import groupby
from datetime import datetime
from heapq import merge


def data(filename: str) -> Iterator[Tuple[datetime, str, ...]]:
    with open(filename) as f:
        for line in f:
            date, *everything_else = line.split(' | ', 2)
            yield datetime.fromisoformat(date), everything_else


def redditmetrics() -> Iterator[Tuple[datetime, int, str, int]]:
    for date, count in data('redditmetrics/subscriber_count'):
        yield date, int(count), 'Redditmetrics', 0


def raspberrypi() -> Iterator[Tuple[datetime, int, str, int]]:
    for date, count in data('rpi/subscriber_count'):
        yield date, int(count), 'Raspberry Pi', 1


def archive() -> Iterator[Tuple[datetime, int, str, int]]:
    for date, count, source in data('archive/subscriber_count'):
        yield date, int(count), source.strip(), 2


def activity() -> Iterator[Tuple[datetime, int, int, str, int]]:
    for date, submissions, comments in data('activity/activity'):
        yield date, int(submissions), int(comments), 'Pushshift API', 3


def generate_data():
    merged = merge(raspberrypi(), redditmetrics(), archive(), activity(),
                   key=lambda x: x[0])

    for date, group in groupby(merged, lambda x: x[0]):
        subscribers = submissions = comments = ''
        sources = set()
        source_ids = set()

        for _, *data, source, source_id in group:
            source_ids.add(source_id)
            sources.add(source)

            if len(data) == 1:
                subscribers = data[0]
            elif len(data) == 2:
                submissions = data[0]
                comments = data[1]
        yield (date, subscribers, submissions, comments, list(sources), list(source_ids))


with open('../data.csv', 'w') as csv, open('../sources.js', 'w') as js:
    csv.write('Date,Subscribers,Submissions,Comments\n')
    js.write('var sources = [\n')
    
    for date, *data, sources, source_ids in generate_data():
        csv.write(f"{date},{','.join(str(x) for x in data)}\n")
        js.write(f"{{text: {sources!r}, id: {source_ids!r}}},\n")
        
    js.write(']')