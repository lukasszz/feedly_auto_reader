import configparser

from FeedlyClient import client
from feedly_auto_reader import reader

reader._logger_setup()
ini = configparser.ConfigParser()
ini.read('config.ini')
fclient = client.FeedlyClient(sandbox=False, token=ini['FEEDLY_USER']['token'])
feeds = reader.get_unread_feeds(fclient)
old_entries = reader.get_unread_entries(fclient, feeds, int(ini['AUTO_READER']['entries_older_than']))
reader.mark_entries_read(old_entries, fclient)
