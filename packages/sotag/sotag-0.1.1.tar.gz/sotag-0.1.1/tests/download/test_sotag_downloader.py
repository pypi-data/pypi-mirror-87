from unittest import TestCase

from sotag.download.sotag_downloader import SOTagDownloader
from sotag.models.tag import SOTagItem


class TestSoTagSearcher(TestCase):

    def test_so_tag_searcher(self):
        searcher = SOTagDownloader()
        print(len(searcher.synonyms_data))
        self.assertTrue(len(searcher.synonyms_data) > 0)
        so_tag_item: SOTagItem = searcher.get_tag_item_for_one_tag("javascript")
        print(so_tag_item.tag_name)
        print(so_tag_item.synonyms)
        print(so_tag_item.short_description)
        self.assertIsNotNone(so_tag_item)
        # searcher.run() # todo make run() has a testable way, not run for all tags.
        searcher.save("test.bin")
