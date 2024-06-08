const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  mode: 'production', // 'development' or 'production'
  entry: './src/scss/styles.scss', // Adjust the entry point if necessary
  output: {
    filename: 'bundle.js',
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
    })
  ],
  devServer: {
    static: {
      directory: path.join(__dirname, 'public')
    },
    compress: true,
    port: 9000
  }
};
