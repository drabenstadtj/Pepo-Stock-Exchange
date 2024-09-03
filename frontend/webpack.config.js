const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const Dotenv = require('dotenv-webpack');

module.exports = {
  mode: process.env.NODE_ENV || 'development', // 'development' or 'production'
  entry: {
    leaderboard: './public/javascripts/leaderboard.js',
    stocks: './public/javascripts/stocks.js',
    trade: './public/javascripts/trade.js'
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'public/javascripts')
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader'
        ]
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        }
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '../stylesheets/style.css'
    }),
    new Dotenv({
      path: path.resolve(__dirname, '../.env'), // Load .env file from the project root
    })
  ],
  devServer: {
    static: {
      directory: path.join(__dirname, 'public')
    },
    compress: true,
    port: process.env.FRONTEND_PORT || 3000
  }
};
