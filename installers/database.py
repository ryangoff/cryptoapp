from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Persisted = declarative_base()

class Watchlist(Persisted):
    __tablename__ = 'watchlist'
    crypto_id = Column(Integer, primary_key=True) #auto increments by default
    name = Column(String(100), nullable=False)
    symbol = Column(String(8), unique=True, nullable=False)
    target = Column(Float, nullable=True)
    price = Column(Float, nullable=True)

class LoginInfo(Persisted):
    __tablename__ = 'login_info'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Cryptocurrency(Persisted):
    __tablename__ = 'cryptocurrencies'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    symbol = Column(String(10), nullable=False, unique=True)
    price_at_entry = Column(Float, nullable=False)

    entries = relationship('PortfolioEntry', back_populates='cryptocurrency')

class PortfolioEntry(Persisted):
    __tablename__ = 'portfolio_entries'
    id = Column(Integer, primary_key=True)
    crypto_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    quantity = Column(Float, nullable=False)
    purchase_date = Column(Date, nullable=False)
    total_investment = Column(Float, nullable=False)

    cryptocurrency = relationship('Cryptocurrency', back_populates='entries')

class CryptoDatabase(object):
    @staticmethod
    def construct_mysql_url(authority, port, database, username, password):
        return f'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}'

    @staticmethod
    def construct_in_memory_url():
        return 'sqlite:///'

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def ensure_tables_exist(self):
        Persisted.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()



