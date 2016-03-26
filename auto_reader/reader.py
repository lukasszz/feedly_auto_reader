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
        f['title'] = r.findall(f['id'])[0]
        feeds.append(f)

    return feeds


def get_unread_entries(client: FeedlyClient, feeds: list, entries_older_than: int):
    old_entries = []
    for feed in feeds:
        entries = client.get_feed_content(FEEDLY_TOKEN, feed['id'])
        for e in entries['items']:
            if e['published'] < (datetime.now() - timedelta(days=entries_older_than)).timestamp() * 1e3:
                old_entries.append(e)
    return old_entries


if __name__ == '__main__':
    ini = configparser.ConfigParser()
    ini.read('config.ini')
    FEEDLY_TOKEN = ini['FEEDLY_USER']['token']
    fclient = FeedlyClient(sandbox=False)
    feeds = get_unread_feeds(fclient)
    old_entries = get_unread_entries(fclient, feeds, int(ini['AUTO_READER']['entries_older_than']))

    print(old_entries)

    # if len(ids) > 0:
    #     client.mark_article_read(FEEDLY_TOKEN, ids)
