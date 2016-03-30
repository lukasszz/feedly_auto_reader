import configparser
import re
from datetime import datetime, timedelta
import logging

from FeedlyClient.client import FeedlyClient


def get_unread_feeds(client: FeedlyClient):
    counts = client.get_counts(client.token)
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
        entries = client.get_feed_content(client.token, feed['id'])
        for e in entries['items']:
            if e['published'] < (datetime.now() - timedelta(days=entries_older_than)).timestamp() * 1e3:
                old_entries.append(e)
    return old_entries


def mark_entries_read(entries: [], client: FeedlyClient, ):
    logger = logging.getLogger('feedly_autor_reader')
    if len(entries) == 0:
        logger.info("No old arctiles to mark as read")

    ids = []
    for e in entries:
        ids.append(e['id'])
        logger.info('%s %s', e['title'], e['originId'])

    client.mark_article_read(client.token, ids)


def _logger_setup():
    logger = logging.getLogger('feedly_autor_reader')
    fh = logging.FileHandler('feedly_autor_reader.log')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)


if __name__ == '__main__':
    _logger_setup()
    ini = configparser.ConfigParser()
    ini.read('config.ini')
    fclient = FeedlyClient(sandbox=False, token=ini['FEEDLY_USER']['token'])
    feeds = get_unread_feeds(fclient)
    old_entries = get_unread_entries(fclient, feeds, int(ini['AUTO_READER']['entries_older_than']))
    mark_entries_read(old_entries, fclient)
