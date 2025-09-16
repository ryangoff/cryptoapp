from unittest import TestCase

from database import CryptoDatabase
from main import WatchlistApp


class TestNewEntry(TestCase):


    def test_add_entry(self):
        url = CryptoDatabase.construct_in_memory_url()
        self.db = CryptoDatabase(url)
        self.db.ensure_tables_exist()
        self.session = self.db.create_session()
        WatchlistApp._new_entry(self.session, 'TestCoin', 'TST', '100')

    def test_add_entry_missing_name(self):
        url = CryptoDatabase.construct_in_memory_url()
        self.db = CryptoDatabase(url)
        self.db.ensure_tables_exist()
        self.session = self.db.create_session()
        WatchlistApp._new_entry(self.session, '', 'TST', '100')

    def test_add_entry_missing_symbol(self):
        url = CryptoDatabase.construct_in_memory_url()
        self.db = CryptoDatabase(url)
        self.db.ensure_tables_exist()
        self.session = self.db.create_session()
        WatchlistApp._new_entry(self.session, 'TestCoin', '', '100')

    def test_add_entry_missing_target(self):
        url = CryptoDatabase.construct_in_memory_url()
        self.db = CryptoDatabase(url)
        self.db.ensure_tables_exist()
        self.session = self.db.create_session()
        WatchlistApp._new_entry(self.session, 'TestCoin', 'TST', None)

    def test_add_entry_missing_all(self):
        url = CryptoDatabase.construct_in_memory_url()
        self.db = CryptoDatabase(url)
        self.db.ensure_tables_exist()
        self.session = self.db.create_session()
        WatchlistApp._new_entry(self.session, '', '', None)
