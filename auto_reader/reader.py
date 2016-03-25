import configparser
import json
import re
from datetime import datetime, timedelta

import requests

from auto_reader.client import FeedlyClient


def get_unread_feeds(client: FeedlyClient):
    counts = client.get_info_type(FEEDLY_TOKEN, 'counts')
    counts = counts['unreadcounts']
    feeds = []
    for f in counts:
        if f['count'] == 0:
            continue
        r = re.compile(r'user/.*?/category/')
        if r.match(f['id']):
            continue

        r = re.compile(r'feed/http://(.*?)/')
        feeds.append({'title': r.findall(f['id'])[0], 'count': f['count']})
        print(f)

    return feeds


def get_unread_entries(client: FeedlyClient, feed: str):
    entries = client.get_feed_content(access_token=FEEDLY_TOKEN, streamId=feed, unreadOnly=True)
    ids = []
    for e in entries['items']:
        if e['published'] < (datetime.now() - timedelta(days=2)).timestamp() * 1e3:
            ids.append(e['id'])
            print("Starszy: " + e["title"])
    if len(ids) > 0:
        client.mark_article_read(FEEDLY_TOKEN, ids)


if __name__ == '__main__':
    ini = configparser.ConfigParser()
    ini.read('config.ini')
    FEEDLY_TOKEN = ini['FEEDLY_USER']['token']
    fclient = FeedlyClient(sandbox=False)
    print(get_unread_feeds(fclient))
    # get_unread_entries(fclient, 'feed/http://planet.python.org/rss20.xml')
