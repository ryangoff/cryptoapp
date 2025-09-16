from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from sqlalchemy.exc import SQLAlchemyError
from database import CryptoDatabase, Cryptocurrency, PortfolioEntry
from pycoingecko import CoinGeckoAPI

coin_gecko_api = CoinGeckoAPI()

class MainMenuScreen(Screen):
    pass

class NewCryptoScreen(Screen):
    def submit_crypto(self):
        name = self.ids.crypto_name.text.strip()
        symbol = self.ids.crypto_symbol.text.strip().upper()
        price = self.ids.crypto_price.text.strip()

        if not name or not symbol or not price:
            self.ids.crypto_message.text = "All fields are required."
            return

        if self.app.session.query(Cryptocurrency).filter_by(symbol=symbol).first():
            self.ids.crypto_message.text = "Symbol already exists."
            return

        try:
            new_crypto = Cryptocurrency(name=name, symbol=symbol, price_at_entry=float(price))
            self.app.session.add(new_crypto)
            self.app.session.commit()
            self.ids.crypto_message.text = "Cryptocurrency added successfully."
            self.ids.crypto_name.text = ''
            self.ids.crypto_symbol.text = ''
            self.ids.crypto_price.text = ''
        except SQLAlchemyError as e:
            self.ids.crypto_message.text = f"Error: {e}"

class NewEntryScreen(Screen):
    def submit_entry(self):
        symbol = self.ids.entry_symbol.text.strip().upper()
        quantity = self.ids.entry_quantity.text.strip()
        purchase_date = self.ids.entry_date.text.strip()

        if not symbol or not quantity or not purchase_date:
            self.ids.entry_message.text = "All fields are required."
            return

        try:
            crypto = self.app.session.query(Cryptocurrency).filter_by(symbol=symbol).first()
            if not crypto:
                self.ids.entry_message.text = "Cryptocurrency not found."
                return

            total_investment = float(quantity) * crypto.price_at_entry
            new_entry = PortfolioEntry(crypto_id=crypto.id, quantity=float(quantity), purchase_date=purchase_date, total_investment=total_investment)
            self.app.session.add(new_entry)
            self.app.session.commit()
            self.ids.entry_message.text = "Portfolio entry added successfully."
            self.ids.entry_symbol.text = ''
            self.ids.entry_quantity.text = ''
            self.ids.entry_date.text = ''
        except SQLAlchemyError as e:
            self.ids.entry_message.text = f"Error: {e}"

class PortfolioValueScreen(Screen):
    def refresh_prices(self):
        try:
            entries = self.app.session.query(PortfolioEntry).all()
            total_value = 0
            total_invested = 0
            summary = self.ids.summary_container
            summary.clear_widgets()
            for entry in entries:
                crypto = self.app.session.query(Cryptocurrency).get(entry.crypto_id)
                current_price = coin_gecko_api.get_price(ids=crypto.symbol.lower(), vs_currencies='usd')
                current_value = current_price[crypto.symbol.lower()]['usd'] * entry.quantity
                total_value += current_value
                total_invested += entry.total_investment
                summary.add_widget(Label(text=f"{crypto.name}: Current Value: ${current_value:.2f}, Invested: ${entry.total_investment:.2f}"))

            overall_change = ((total_value - total_invested) / total_invested) * 100 if total_invested > 0 else 0
            summary.add_widget(Label(text=f"Total Portfolio Value: ${total_value:.2f}, Total Invested: ${total_invested:.2f}, Overall Change: {overall_change:.2f}%"))
        except Exception as e:
            print(f"Error refreshing prices: {e}")

class PortfolioApp(App):
    def __init__(self, password = None, **kwargs):
        super(PortfolioApp, self).__init__(**kwargs)
        self.password = password
        if not self.password:
            password = input("Enter your password: ")
        url = CryptoDatabase.construct_mysql_url('localhost', 3306, 'cryptodatabase', 'root', password)
        self.database = CryptoDatabase(url)
        self.session = self.database.create_session()
        self.database.ensure_tables_exist()

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(NewCryptoScreen(name='new_crypto'))
        sm.add_widget(NewEntryScreen(name='new_entry'))
        sm.add_widget(PortfolioValueScreen(name='portfolio_value'))
        for screen in sm.screens:
            screen.app = self
        return sm

if __name__ == '__main__':
    PortfolioApp().run()