from sys import stderr
from kivy.app import App
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from sqlalchemy.exc import SQLAlchemyError
from pycoingecko import CoinGeckoAPI

coin_gecko_api = CoinGeckoAPI()

from database import CryptoDatabase, Watchlist


class WatchlistApp(App):
    def __init__(self, password=None, **kwargs):
        super(WatchlistApp, self).__init__(**kwargs)
        if password is None:
            password = input("Enter your password: ")
        url = CryptoDatabase.construct_mysql_url('localhost', 3306, 'cryptodatabase', 'root', password)
        self.watchlist = CryptoDatabase(url)
        self.session = self.watchlist.create_session()
        inspector.create_inspector(Window, self)

    def submit(self):
        try:

            screen = self.root.get_screen('entry')
            name = screen.ids.name_input.text.strip()
            symbol = screen.ids.symbol_input.text.strip().upper()
            target = screen.ids.target_input.text.strip().upper()

            if not name or not symbol or not target:
                print("A name, target, and a symbol are required to submit.")
                return

            if self.session.query(Watchlist).filter_by(symbol=symbol).first():
                print(f"Symbol '{symbol}' already exists in the watchlist.")
                return

            self.session.add(Watchlist(name=name, symbol=symbol, target=target))
            self.session.commit()
            submit = self.root.get_screen('entry')
            self.refresh()
            submit.ids.success_submit.text = f"Successfully added {name} to watchlist."
            self.root.get_screen('entry').ids.name_input.text = ''
            self.root.get_screen('entry').ids.symbol_input.text = ''
            self.root.get_screen('entry').ids.target_input.text = ''

        except SQLAlchemyError as exception:
            print('Failed to add to watchlist', exception)

    def _new_entry(session, name, symbol, target):
        session.add(Watchlist(name=name, symbol=symbol, target=target))
        session.commit()

    def wipe_popup_labels(self):
        refresh = self.root.get_screen('refresh')
        submit = self.root.get_screen('entry')
        refresh.ids.refresh_success.text = ""
        submit.ids.success_submit.text = ""

    def refresh(self):
        try:
            screen = self.root.get_screen('refresh')
            watchlist_prices = self.session.query(Watchlist).all()

            for entry in watchlist_prices:
                coin_id = entry.name.lower()
                price_data = coin_gecko_api.get_price(ids=coin_id, vs_currencies='usd')
                price = price_data.get(coin_id, {}).get('usd')

                if price is not None:
                    entry.price = price
                    print(f"{entry.name}: ${price}")
                else:
                    print(f"{entry.name} is not available")

            self.session.commit()
            self.fill_watchlist()
            screen.ids.refresh_success.text = "Successfully refreshed watchlist"

        except Exception as e:
            print(f"Error while refreshing prices: {e}")
    def fill_watchlist(self):
        try:
            screen = self.root.get_screen('view')
            container = screen.ids.watchlist

            container.clear_widgets()

            watchlist_entries = self.session.query(Watchlist).all()

            for entry in watchlist_entries:
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)

                name_label = Label(text=entry.name, font_size=50, color = (0.4, 0.7, 1, 1))
                symbol_label = Label(text=entry.symbol, font_size=50, color = (0.2, 0.4, 0.8, 1))
                if entry.price is not None and entry.target < entry.price:
                    target_label = Label(text=f"${entry.target}", font_size=50, color=(0.0, 0.4, 0.0, 1))
                else:
                    target_label = Label(text=f"${entry.target}", font_size=50, color=(1, 0.84, 0, 1))

                price_label = Label(text=f"${entry.price}" if entry.price is not None else "N/A", font_size=50,color=(0.2, 0.4, 0.8, 1))


                row.add_widget(name_label)
                row.add_widget(symbol_label)
                row.add_widget(price_label)
                row.add_widget(target_label)

                container.add_widget(row)

        except Exception as e:
            print(f"Failed to populate watchlist: {e}")


    def move_entry_up(self):
        pass #Reorders the selected entry and moves it up by one unit

    def move_entry_down(self):
        pass #Reorders the selected entry and moves it down by one unit


def main():
    try:
        watchlist = WatchlistApp()
        watchlist.run()

    except SQLAlchemyError as exception:
        print('Database connection failed.', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)


if __name__ == '__main__':
    app = WatchlistApp()
    app.run()
    main()
