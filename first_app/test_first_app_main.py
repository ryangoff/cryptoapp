import unittest
from unittest.mock import MagicMock
from first_app_main import NewCryptoScreen, NewEntryScreen, Cryptocurrency

class TestNewCryptoScreen(unittest.TestCase):
    def setUp(self):
        self.screen = NewCryptoScreen(name='test_new_crypto')
        self.screen.ids = {
            'crypto_name': MagicMock(text='Bitcoin'),
            'crypto_symbol': MagicMock(text='BTC'),
            'crypto_price': MagicMock(text='30000'),
            'crypto_message': MagicMock()
        }
        self.screen.app = MagicMock()
        self.screen.app.session.query.return_value.filter_by.return_value.first.return_value = None

    def test_submit_crypto_success(self):
        self.screen.submit_crypto()
        self.screen.app.session.add.assert_called()
        self.screen.app.session.commit.assert_called()
        self.assertIn("Cryptocurrency added successfully", self.screen.ids['crypto_message'].text)

class TestNewEntryScreen(unittest.TestCase):
    def setUp(self):
        self.screen = NewEntryScreen(name='test_new_entry')
        self.screen.ids = {
            'entry_symbol': MagicMock(text='BTC'),
            'entry_quantity': MagicMock(text='2'),
            'entry_date': MagicMock(text='2024-01-01'),
            'entry_message': MagicMock()
        }
        self.screen.app = MagicMock()
        self.mock_crypto = Cryptocurrency(id=1, name='Bitcoin', symbol='BTC', price_at_entry=30000)
        self.screen.app.session.query.return_value.filter_by.return_value.first.return_value = self.mock_crypto

    def test_submit_entry_success(self):
        self.screen.submit_entry()
        self.screen.app.session.add.assert_called()
        self.screen.app.session.commit.assert_called()
        self.assertIn("Portfolio entry added successfully", self.screen.ids['entry_message'].text)

if __name__ == '__main__':
    unittest.main()