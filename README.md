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
