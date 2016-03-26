import configparser
import re
from datetime import datetime, timedelta


from FeedlyClient.client import FeedlyClient


def get_unread_feeds(client: FeedlyClient):
    counts = client.get_counts(FEEDLY_TOKEN)
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


def get_unread_entries(client: FeedlyClient, feed: str, entries_older_than):
    entries = client.get_feed_content(FEEDLY_TOKEN, feed)
    old_entries = []
    for e in entries['items']:
        if e['published'] < (datetime.now() - timedelta(days=entries_older_than)).timestamp() * 1e3:
            old_entries.append(e)
    return old_entries


if __name__ == '__main__':
    ini = configparser.ConfigParser()
    ini.read('config.ini')
    FEEDLY_TOKEN = ini['FEEDLY_USER']['token']
    fclient = FeedlyClient(sandbox=False)
    #    print(get_unread_feeds(fclient))
    old_entries = get_unread_entries(fclient, 'feed/http://planet.python.org/rss20.xml', ini['AUTOREADER']['entries_older_than'])

    # if len(ids) > 0:
    #     client.mark_article_read(FEEDLY_TOKEN, ids)
