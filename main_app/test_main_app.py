from unittest import TestCase

from database import CryptoDatabase
from startup import KivyStartupApp


class TestNewEntry(TestCase):


    def test_add_profile(self):
        url = CryptoDatabase.construct_in_memory_url()
        self.db = CryptoDatabase(url)
        self.db.ensure_tables_exist()
        self.session = self.db.create_session()
        app = KivyStartupApp()
        app.build()
        app.profile(0, name='killer')

    def test_missing_name(self):
        url = CryptoDatabase.construct_in_memory_url()
        self.db = CryptoDatabase(url)
        self.db.ensure_tables_exist()
        self.session = self.db.create_session()
        app = KivyStartupApp()
        app.build()
        app.profile(0, name=None)

    def test_name_exist(self):
        url = CryptoDatabase.construct_in_memory_url()
        self.db = CryptoDatabase(url)
        self.db.ensure_tables_exist()
        self.session = self.db.create_session()
        app = KivyStartupApp()
        app.build()
        app.profile(0, name='Ryan')