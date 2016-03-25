import configparser
import json
import re

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
    url = client._get_endpoint('v3/streams/ids')
    params = dict(streamId=feed, unreadOnly=True)
    headers = {
        'Authorization': 'OAuth ' + FEEDLY_TOKEN
    }
    res = requests.get(url=url,
                       params=json.dumps(params),
                       headers=headers)
    print(url)
    print(res)

    res = client.get_feed_content(streamId=feed, unreadOnly=True)
    print(res)


if __name__ == '__main__':
    ini = configparser.ConfigParser()
    ini.read('config.ini')
    FEEDLY_TOKEN = ini['FEEDLY_USER']['token' \
                                      '']
    fclient = FeedlyClient(sandbox=False)
    print(get_unread_feeds(fclient))
    #get_unread_entries(fclient, 'feed/http://art-of-software.blogspot.com/feeds/posts/default')
