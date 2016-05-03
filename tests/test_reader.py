import unittest
import feedly_auto_reader.reader as far


class TestFetchTitle(unittest.TestCase):
    def test_https(self):
        fixture = [{'fid': 'feed/http://www.geekweek.pl/kategoria/nauka/feed', 'expected': 'geekweek.pl'},
                   {'fid': 'feed/http://feeds.feedburner.com/ABCInwestowaniaiFinanseOsobiste',
                    'expected': 'ABCInwestowaniaiFinanseOsobiste'},
                   {'fid': 'feed/http://rss.swiatczytnikow.pl/SwiatCzytnikow', 'expected': 'swiatczytnikow.pl'},
                   {'fid': 'feed/http://allegro.pl/rss.php?feed=webapi_news&gen=1&all=1', 'expected': 'allegro.pl'},
                   {'fid': 'feed/https://arkos.io/feed/', 'expected': 'arkos.io'}]

        for f in fixture:
            self.assertEquals(f['expected'], far._build_title(f['fid']))
