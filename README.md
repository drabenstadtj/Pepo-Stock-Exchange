# Simulated Stock Market Backend

## Overview

This project is a simulated stock market backend built using Flask, MongoDB, and Python. It includes user authentication, stock management, transaction handling, and portfolio management functionalities. The stock prices are dynamically updated based on Google Trends data to simulate market interest.

## Directory Structure

```
.
├── backend
│ ├── app
│ │ ├── init.py
│ │ ├── config.py
│ │ ├── routes
│ │ │ ├── init.py
│ │ │ ├── auth.py
│ │ │ ├── stocks.py
│ │ │ ├── transactions.py
│ │ │ └── portfolio.py
│ │ ├── services
│ │ │ ├── init.py
│ │ │ ├── user_service.py
│ │ │ ├── stock_service.py
│ │ │ └── transaction_service.py
│ ├── venv
│ ├── .env
│ ├── pycache
│ └── scripts
│ └── update_stock_prices.py
├── frontend
│ ├── node_modules
│ ├── .env
│ └── pycache
└── README.md
```

## Features

- **User Authentication**: Users can register and log in to their accounts.
- **Stock Management**: View and manage stocks, including fetching current stock prices and sectors.
- **Transactions**: Buy and sell stocks, with transactions logged in the database.
- **Portfolio Management**: Users can view their portfolio, including owned stocks and balances.
- **Dynamic Stock Prices**: Stock prices are updated hourly based on Google Trends data to reflect market interest.

## API Endpoints

### Authentication

- `POST /auth/register`: Register a new user.
- `GET /auth/get_user_id`: Fetch user ID by username.

### Stocks

- `GET /stocks/`: Fetch all stocks.

### Transactions

- `POST /transactions/buy`: Buy a stock.
- `POST /transactions/sell`: Sell a stock.
- `GET /transactions/`: Fetch all transactions or transactions for a specific user.

### Portfolio

- `GET /portfolio/`: Fetch the user's portfolio by user ID.

## Scheduled Tasks

- **Stock Price Update**: A script (`scripts/update_stock_prices.py`) is set up to update stock prices every 30 seconds based on Google Trends data. This script can be scheduled to run as a background task.
