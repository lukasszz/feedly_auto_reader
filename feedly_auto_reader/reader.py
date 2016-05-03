import logging
import re
from datetime import datetime, timedelta

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

        f['title'] = _build_title(f['id'])[0]
        r.findall(f['id'])
        feeds.append(f)

    return feeds


def _build_title(feed_id):
    prefixes = ['feeds\.feedburner\.com/', 'www\.', 'rss\.']
    remove_prefix = ''
    for p in prefixes:
        remove_prefix += '(?:' + p + ')?'

    r = re.compile(r'feed/https?://' + remove_prefix + '([^/]*)')
    g = r.findall(feed_id)
    return g[0]


def get_unread_entries(client: FeedlyClient, feeds: list, entries_older_than: int):
    old_entries = []
    for feed in feeds:
        entries = client.get_feed_content(client.token, feed['id'])
        for e in entries['items']:
            if e['published'] < (datetime.now() - timedelta(days=entries_older_than)).timestamp()*1e3:
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
