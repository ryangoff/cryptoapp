from sys import stderr
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from database import CryptoDatabase, Cryptocurrency, PortfolioEntry, LoginInfo


def add_starter_data(session):
    # Adds sample user
    ryan = LoginInfo(name='Ryan')
    session.add(ryan)

    #Adds sample cryptocurrencies
    btc = Cryptocurrency(
        name='Bitcoin',
        symbol='BTC',
        price_at_entry=50000.00,

    )

    eth = Cryptocurrency(
        name='Ethereum',
        symbol='ETH',
        price_at_entry=3000.00,

    )

    session.add_all([btc, eth])
    session.flush()

    # Adds sample portfolio entries
    btc_entry = PortfolioEntry(
        crypto_id=btc.id,
        quantity=0.5,
        purchase_date=date(2023, 1, 1),
        total_investment=0.5 * btc.price_at_entry
    )

    eth_entry = PortfolioEntry(
        crypto_id=eth.id,
        quantity=2.0,
        purchase_date=date(2023, 1, 15),
        total_investment=2.0 * eth.price_at_entry
    )

    session.add_all([btc_entry, eth_entry])


def main(password=None):
    try:
        if password is None:
            password = input('MySQL Password: ')

        url = CryptoDatabase.construct_mysql_url(
            authority='localhost',
            port=3306,
            database='cryptodatabase',
            username='root',
            password=password
        )

        cryptodb = CryptoDatabase(url)
        cryptodb.ensure_tables_exist()
        print('Tables created successfully.')

        session = cryptodb.create_session()
        add_starter_data(session)
        session.commit()
        print('Sample data added successfully.')

    except SQLAlchemyError as exception:
        print('Database setup failed.', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)
    except Exception as e:
        print(f'An unexpected error occurred: {e}', file=stderr)
        exit(1)


if __name__ == '__main__':
    main()




