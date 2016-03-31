import configparser

from FeedlyClient.client import FeedlyClient
from feedly_auto_reader.reader import _logger_setup, get_unread_feeds, get_unread_entries, mark_entries_read

_logger_setup()
ini = configparser.ConfigParser()
ini.read('config.ini')
fclient = FeedlyClient(sandbox=False, token=ini['FEEDLY_USER']['token'])
feeds = get_unread_feeds(fclient)
old_entries = get_unread_entries(fclient, feeds, int(ini['AUTO_READER']['entries_older_than']))
mark_entries_read(old_entries, fclient)
