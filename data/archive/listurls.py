from time import sleep

import requests
import webbrowser


SEARCH_URL = ( # https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md
    'http://web.archive.org/cdx/search/cdx' # Wayback CDX Server
    '?url=www.reddit.com/r/uruguay'
    '&matchType=prefix'
    '&fl=timestamp,original'
)

def process_timestamp(timestamp):
    year = timestamp[:4]
    month = timestamp[4:6]
    day = timestamp[6:8]
    hour = timestamp[8:10]
    minutes = timestamp[10:12]
    seconds = timestamp[12:14]

    return f'{year}-{month}-{day} {hour}:{minutes}:{seconds}'


while True:
    try:
        lines = requests.get(SEARCH_URL).text.splitlines()
    except requests.exceptions.ConnectionError:
        sleep(2)
    else:
        break


data = (line.split(' ', 1) for line in lines)

for timestamp, original in data:
    time = process_timestamp(timestamp)
    url = f'https://web.archive.org/web/{timestamp}/{original}'
    print(time, url)
    webbrowser.open(url)
    subs = int(input('Subscribers = '))