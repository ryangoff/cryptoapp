# Crypto Tracking App

To run the installer you must run database_installer.py AFTER creating a new SQL database named cryptodatabase, if 
successful you will see Records Created & Tables Created. If you want a clean load of the database run table_dropper.py
to drop the tables and it prompts you if you would like to run the installer after they have been wiped.

Crypto Portfolio Tracker is a simplified app that helps users monitor their cryptocurrency investments. A user can 
create a portfolio by adding various cryptocurrencies by filling in the name, symbol, and purchase particulars of the 
coin. Investment totals are calculated automatically and prices are fetched from the CoinGecko API with the click of a 
button. Currently, the primary functions are working: adding coins, recording transactions, and viewing a portfolio 
along with profit and loss percentages. All information is kept safe in a MySQL database with the appropriate table 
relations. Some additional features include editing and deleting entries, advanced visual representations of portfolio 
growth, and are being worked on at the moment. The app performs basic error checks. The design is minimalistic in that 
all the crucial elements are displayed and all calculations are performed behind the scenes, presented in big-picture 
form in order to provide investment insights.

The crypto watchlist app allows you to add coins of your choice via input boxes on the 'New Watchlist Entry' screen.
requiring both a name and symbol with an optional target price to track your coin until a certain point. To update the
prices of the coins you have entered head to the refresh screen and press the 'Refresh Prices' button to pull the latest
price from CoinGecko. To view the coins in your watchlist head to the 'View Watchlist' screen, and you will see your entry
name, symbol, price, and target price if you set one. The target price will appear green if your target has exceeded the
current price letting you know that the target has been reached, but until then it will appear gold.

Watchlist app completeness:

- Missing reordering functionality
- Needs popup for failed entry

Portfolio app completeness:

- All core functionality added
- Missing advanced error handling and update/delete support

Main app completeness:

- Missing popup for failed username entry
- Username linking still needs to be added
- A button to be able to get back from the apps needs to be added

Instructions for building and running the apps, including any required dependencies and commands to create the database.
To run the apps you must first run the database_installer.py, have Kivy installed, SQLAlchemy, and a database
named cryptodatabase. Next run startup.py and enter your MySQL password, from here you can navigate to any of the apps
easily and you do not need to type it in again until your next run of the app. 


Created by Sean, Levi , and Ryan
