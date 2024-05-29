# Pepo Exchange

The simulated stock market application is a comprehensive web-based platform designed to provide users with a realistic stock trading experience. This project integrates a Flask-based backend with a MongoDB database and an Express.js frontend using Pug templating.

The backend is responsible for handling all the business logic, data processing, and user interactions with the database. It includes features like user authentication (registration and login), stock management (fetching current stock prices and sectors), transaction handling (buying and selling stocks), and portfolio management (viewing owned stocks and balances). Stock prices are dynamically updated based on Google Trends data to simulate real market interest, making the application more engaging and realistic.

Scheduled tasks are implemented to update stock prices every 30 seconds, ensuring that the data remains current. This involves a script that fetches the latest trends and adjusts stock prices accordingly. The backend is structured with clear separation of concerns, organized into routes, services, and scripts to ensure maintainability and scalability.

The frontend, built with Express.js and Pug, provides a user-friendly interface where users can sign up, log in, manage their portfolios, view stock information, and perform trades. Each part of the application is neatly organized into Pug templates for consistent layout and design. The interface is designed to be intuitive and responsive, offering a seamless user experience.

## Frontend

## Overview

The frontend of the simulated stock market application is built with Express.js and Pug templating to provide an intuitive and engaging user interface. It includes user authentication pages (sign up and sign in), a dashboard for viewing and managing portfolios, a trading page for buying and selling stocks, and stock information pages. The frontend uses Pug templates for a consistent look and feel, with partials for reusable elements like the header and navigation. It communicates with the backend through API calls to ensure users have access to the latest data, making stock trading activities smooth and responsive.

## Directory Structure

```
.
├── frontend
│ ├── views
│ │ ├── signup.pug
│ │ ├── signin.pug
│ │ ├── dashboard.pug
│ │ ├── about.pug
│ │ ├── trade.pug
│ │ ├── stocks.pug
│ │ ├── index.pug
│ │ ├── layout.pug
│ │ ├── _header.pug
│ │ ├── _navigation.pug
│ │ └── _clock.pug
│ ├── public
│ │ └── stylesheets
│ │     └── style.css
│ └── app.js
└── README.md
```

## Features

- **User Authentication**: Users can register and log in to their accounts.
- **Dashboard**: View and manage user portfolio, including owned stocks and balances.
- **Stock Management**: View available stocks and their current prices.
- **Transactions**: Buy and sell stocks through a user-friendly interface.
- **About Page**: Information about the application and its functionalities.
- **Responsive Design**: Ensures usability across different devices and screen sizes.

## Pages and Templates

### Authentication

- **signup.pug**: Template for user registration.
- **signin.pug**: Template for user login.

### Dashboard

- **dashboard.pug**: Displays user portfolio and options for trading.

### Stocks

- **stocks.pug**: Displays available stocks and their current prices.
- **trade.pug**: Template for executing buy and sell transactions.

### Other Pages

- **index.pug**: Main landing page template.
- **about.pug**: Provides information about the application.

### Layout and Partials

- **layout.pug**: Base layout template for consistent header and footer.
- **_header.pug**: Partial template for the header.
- **_navigation.pug**: Partial template for navigation.
- **_clock.pug**: Partial template for displaying the current time.

## Backend

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
