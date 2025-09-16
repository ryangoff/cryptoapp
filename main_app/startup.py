from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.modules import inspector
from kivy.core.window import Window

from sqlalchemy.exc import SQLAlchemyError
from database import CryptoDatabase, LoginInfo

import first_app
from first_app import first_app_main
from first_app.first_app_main import PortfolioApp
from watchlist_app.main import WatchlistApp

class KivyStartupApp(App):
    def __init__(self, **kwargs):
        super(KivyStartupApp, self).__init__(**kwargs)
        self.password = input("Enter your password: ")
        url = CryptoDatabase.construct_mysql_url('localhost', 3306, 'cryptodatabase', 'root', self.password)
        self.watchlist = CryptoDatabase(url)
        self.session = self.watchlist.create_session()
        inspector.create_inspector(Window, self)

    def build(self):
        inspector.create_inspector(Window, self)
        root = Builder.load_file("KivyStartup.kv")  # or build root manually
        self.root = root
        self.fill_profile()
        return root

    def profile_test(self, name):
        Clock.schedule_once(self.profile(name), 0)

    def profile(self, dt=None, name=None):
        try:
            screen = self.root.get_screen('login')
            if name is None:
                name = screen.ids.username.text.strip()

            if not name:
                self.root.get_screen('login').ids.message.text = 'Please enter a username.'
                return
            if self.session.query(LoginInfo).filter_by(name=name).first():
                self.root.get_screen('login').ids.message.text = f"Name '{name}' already exists in the watchlist."
                return
            self.session.add(LoginInfo(name=name))
            self.session.commit()
            self.root.get_screen('login').ids.username.text = ''
            self.fill_profile()
            self.root.get_screen('login').ids.message.text = 'Username successfully added.'
        except SQLAlchemyError as e:
            self.root.ids.message.text = 'Failed to add to database', e

    def fill_profile(self):
        try:
            screen = self.root.get_screen('login')
            container = screen.ids.dropdown

            container.clear_widgets()

            login_entries = self.session.query(LoginInfo).all()
            for entry in login_entries:
                if entry.name in self.root.get_screen('login').ids.dropdown.values:
                    pass
                else:
                    self.root.get_screen('login').ids.dropdown.values.append(entry.name)
        except SQLAlchemyError as e:
            self.root.get_screen('login').ids.message.text = f"Failed to populate username: '\n{e}'"

    def open_watchlist(self):
        Clock.schedule_once(self.launch_watchlist, 0)

    def launch_watchlist(self, dt):
        self.stop()
        WatchlistApp(password=self.password).run()

    def open_portfolio(self):
        Clock.schedule_once(self.launch_portfolio, 0)

    def launch_portfolio(self, dt):
        self.stop()
        PortfolioApp(password=self.password).run()




if __name__ == '__main__':
    app = KivyStartupApp()
    app.run()