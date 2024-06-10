# Pepo Stock Exchange

## Description

Pepo Exchange is a simulated stock market application that provides users with a realistic stock trading experience. This web-based platform integrates a Flask-based backend with a MongoDB database and an Express.js frontend using Pug templating.

The backend handles all business logic, data processing, and user interactions with the database. Key features include user authentication (registration and login), stock management (fetching current stock prices and sectors), transaction handling (buying and selling stocks), and portfolio management (viewing owned stocks and balances). Stock prices are dynamically updated based on Google Trends data to simulate real market interest, making the application more engaging and realistic.

Scheduled tasks update stock prices every hour, ensuring the data remains current. The backend is structured with clear separation of concerns, organized into routes, services, and scripts to ensure maintainability and scalability.

The frontend, built with Express.js and Pug, provides a user-friendly interface where users can sign up, log in, manage their portfolios, view stock information, and perform trades. The interface is designed to be intuitive and responsive.

## Features

- User Authentication (Registration and Login)
- Stock Management (Fetch Current Prices and Sectors)
- Transaction Handling (Buy and Sell Stocks)
- Portfolio Management (View Owned Stocks and Balances)
- Dynamic Stock Prices based on Google Trends Data
- Scheduled Tasks to Update Stock Prices

## File Structure

```
📦Pepo-Stock-Exchange
┣ 📂.git
┣ 📂backend
┃ ┣ 📂app
┃ ┃ ┣ 📂routes
┃ ┃ ┃ ┣ 📜auth.py
┃ ┃ ┃ ┣ 📜leaderboard.py
┃ ┃ ┃ ┣ 📜portfolio.py
┃ ┃ ┃ ┣ 📜stocks.py
┃ ┃ ┃ ┣ 📜transactions.py
┃ ┃ ┃ ┗ 📜__init__.py
┃ ┃ ┣ 📂services
┃ ┃ ┃ ┣ 📜leaderboard_service.py
┃ ┃ ┃ ┣ 📜stock_service.py
┃ ┃ ┃ ┣ 📜transaction_service.py
┃ ┃ ┃ ┣ 📜trends_service.py
┃ ┃ ┃ ┗ 📜user_service.py
┃ ┃ ┣ 📜config.py
┃ ┃ ┗ 📜__init__.py
┃ ┣ 📜requirements.txt
┃ ┣ 📜run.py
┃ ┗ 📜wsgi.py
┣ 📂frontend
┃ ┣ 📂config
┃ ┃ ┗ 📜config.js
┃ ┣ 📂public
┃ ┃ ┣ 📂images
┃ ┃ ┣ 📂javascripts
┃ ┃ ┃ ┣ 📜bundle.js
┃ ┃ ┃ ┣ 📜leaderboard.js
┃ ┃ ┃ ┣ 📜stocks.js
┃ ┃ ┃ ┗ 📜trade.js
┃ ┃ ┗ 📂stylesheets
┃ ┣ 📂src
┃ ┃ ┗ 📂scss
┃ ┃ ┃ ┣ 📜main.js
┃ ┃ ┃ ┣ 📜styles.scss
┃ ┃ ┃ ┗ 📜_variables.scss
┃ ┣ 📂views
┃ ┃ ┣ 📜about.pug
┃ ┃ ┣ 📜index.pug
┃ ┃ ┣ 📜layout.pug
┃ ┃ ┣ 📜leaderboard.pug
┃ ┃ ┣ 📜signin.pug
┃ ┃ ┣ 📜signup.pug
┃ ┃ ┣ 📜stocks.pug
┃ ┃ ┣ 📜trade.pug
┃ ┃ ┣ 📜_clock.pug
┃ ┃ ┣ 📜_header.pug
┃ ┃ ┗ 📜_navigation.pug
┃ ┣ 📜app.js
┃ ┣ 📜package-lock.json
┃ ┣ 📜package.json
┃ ┗ 📜webpack.config.js
┣ 📂utility
┃ ┣ 📂data
┃ ┃ ┣ 📜initialize_stocks.py
┃ ┃ ┣ 📜initial_data.json
┃ ┃ ┗ 📜StockNames.xlsx
┃ ┣ 📂stock_updater
┃ ┃ ┣ 📜trends_updater.py
┃ ┃ ┗ 📜update_stock_prices.py
┃ ┗ 📜test.py
┣ 📜.gitignore
┗ 📜README.md
```

##API Documentation
###Authentication

     - POST /auth/register
        Registers a new user.
        Request body: { "username": "your_username", "password": "your_password" }
        Response: { "message": "User registered successfully" }

     - POST /auth/verify_credentials
        Verifies user credentials and issues a JWT token.
        Request body: { "username": "your_username", "password": "your_password" }
        Response: { "message": "Credentials verified", "token": "your_jwt_token" }

###Portfolio

     - GET /portfolio/stocks
        Fetches the user's portfolio.
        Requires a valid JWT token.
        Response: JSON array of user's stocks.

     - GET /portfolio/balance
        Fetches the user's balance.
        Requires a valid JWT token.
        Response: { "balance": user_balance }

     - GET /portfolio/assets_value
        Fetches the total value of the user's assets.
        Requires a valid JWT token.
        Response: { "assets_value": total_assets_value }

###Stocks

     - GET /stocks/
        Fetches all stocks.
        Response: JSON array of stocks.

     - GET /stocks/
        Fetches the current price of a stock.
        Response: { "symbol": "stock_symbol", "price": stock_price }

###Transactions

     - POST /transactions/buy
        Buys a stock.
        Request body: { "stock_symbol": "symbol", "quantity": quantity }
        Requires a valid JWT token.
        Response: { "message": "Stock purchased successfully" }

     - POST /transactions/sell
        Sells a stock.
        Request body: { "stock_symbol": "symbol", "quantity": quantity }
        Requires a valid JWT token.
        Response: { "message": "Stock sold successfully" }

###Configuration

     - Environment Variables:
        Ensure all required environment variables are set in the .env files in both the backend and frontend directories.