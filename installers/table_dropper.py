# INSTEAD OF HAVING TO CONSTANTLY MANUALLY DROP
# TABLES THIS ALSO PROMPTS IF YOU WANT TO REINSTALL THE TABLES FRESH
# THIS IS NOT A PROJECT REQUIREMENT IT IS JUST FOR CONVENIENCE

from sqlalchemy import create_engine
from database import Persisted, CryptoDatabase
import database_installer


def drop_tables(database_url):
    engine = create_engine(database_url)
    Persisted.metadata.drop_all(engine)


if __name__ == '__main__':
    password = input('Enter your password: ')
    db_url = CryptoDatabase.construct_mysql_url(
        authority='localhost',
        port='3306',
        database='cryptodatabase',
        username='root',
        password= password
    )


    drop_tables(db_url)
    print("Tables dropped successfully.")

    install = input('Would you like to install the tables again? (y/n): ')
    if install == 'y':
        database_installer.main(password)
    else:
        exit()
