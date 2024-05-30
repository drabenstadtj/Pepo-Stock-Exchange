const express = require('express');
const session = require('express-session');
const debug = require('debug')('app');
const axios = require('axios');
const path = require('path');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'views'));

app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Configure session middleware
app.use(session({
  secret: process.env.SESSION_SECRET || 'your-secret-key',
  resave: false,
  saveUninitialized: true,
  cookie: {
    sameSite: 'None', // Ensures the cookie is sent in all contexts
    secure: process.env.NODE_ENV === 'production', // Set to true in production environment
    maxAge: 60000
  }
}));

// Middleware to check if the user is logged in
const requireLogin = (req, res, next) => {
  if (req.session && req.session.user) {
    next();
  } else {
    debug('User not logged in, redirecting to /signin');
    res.redirect('/signin');
  }
};

// Routes
app.get('/signup', (req, res) => {
  res.render('signup', { user: req.session.user });
});

app.post('/signup', async (req, res) => {
  const { username, password } = req.body;
  try {
    const response = await axios.post('http://localhost:5000/auth/register', { username, password });
    if (response.data.message === 'User registered successfully') {
      req.session.user = username;
      debug(`User ${username} registered successfully`);
      res.redirect('/');
    } else {
      debug(`Signup failed for user ${username}: ${response.data.message}`);
      res.send('Signup failed!');
    }
  } catch (error) {
    debug(`Signup error for user ${username}: ${error.message}`);
    res.status(500).send('Signup failed!');
  }
});

app.get('/signin', (req, res) => {
  const error = req.query.error;
  res.render('signin', { error, user: req.session.user });
});

app.post('/signin', async (req, res) => {
  const { username, password } = req.body;
  try {
    const response = await axios.post('http://localhost:5000/auth/verify_credentials', { username, password });
    if (response.data.message === 'Credentials verified') {
      req.session.user = username;
      debug(`User ${username} signed in successfully`);
      res.redirect('/');
    } else {
      debug(`Sign in failed for user ${username}: Invalid credentials`);
      res.redirect('/signin?error=Invalid username or password');
    }
  } catch (error) {
    debug(`Sign in error for user ${username}: ${error.message}`);
    res.redirect('/signin?error=Invalid username or password');
  }
});

app.get('/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      debug(`Logout error: ${err.message}`);
      return res.redirect('/');
    }
    res.clearCookie('connect.sid');
    debug(`User logged out successfully`);
    res.redirect('/signin');
  });
});

app.get('/', requireLogin, (req, res) => {
  debug(`Rendering home page for user ${req.session.user}`);
  res.render('index', { user: req.session.user });
});

app.get('/about', requireLogin, (req, res) => {
  debug(`Rendering about page for user ${req.session.user}`);
  res.render('about', { user: req.session.user });
});

app.get('/dashboard', requireLogin, async (req, res) => {
  try {
    const response = await axios.get('http://localhost:5000/auth/get_user_id', {
      params: { username: req.session.user }
    });
    const user_id = response.data._id;

    const portfolioResponse = await axios.get('http://localhost:5000/portfolio/stocks', {
      params: { user_id }
    });

    const balanceResponse = await axios.get('http://localhost:5000/portfolio/balance', {
      params: { user_id }
    });

    const portfolio = portfolioResponse.data;
    const balance = balanceResponse.data;

    debug(`Fetched portfolio and balance for user ${req.session.user}`);
    res.render('dashboard', { user: req.session.user, portfolio, balance });
  } catch (error) {
    debug(`Error fetching portfolio for user ${req.session.user}: ${error.message}`);
    res.status(500).send("Internal Server Error");
  }
});

app.get('/trade', requireLogin, async (req, res) => {
  try {
    const response = await axios.get('http://localhost:5000/auth/get_user_id', {
      params: { username: req.session.user }
    });
    const user_id = response.data._id;

    const portfolioResponse = await axios.get('http://localhost:5000/portfolio/stocks', {
      params: { user_id }
    });

    const balanceResponse = await axios.get('http://localhost:5000/portfolio/balance', {
      params: { user_id }
    });

    const portfolio = portfolioResponse.data;
    const balance = balanceResponse.data;

    debug(`Fetched portfolio and balance for user ${req.session.user}`);
    res.render('trade', { user: req.session.user, user_id: user_id, portfolio, balance });
  } catch (error) {
    debug(`Error fetching portfolio for user ${req.session.user}: ${error.message}`);
    res.status(500).send("Internal Server Error");
  }
});

app.get('/stocks', requireLogin, async (req, res) => {
  try {
    const response = await axios.get('http://localhost:5000/stocks');
    const stocks = response.data;

    debug(`Fetched stocks data`);
    res.render('stocks', { stocks, user: req.session.user });
  } catch (error) {
    debug(`Error fetching stocks data: ${error.message}`);
    res.status(500).send("Internal Server Error");
  }
});

// Error handler
app.use((err, req, res, next) => {
  debug(`Internal Server Error: ${err.message}`);
  console.error(err.stack); // Log the stack trace to the console
  res.status(500).send('Internal Server Error');
});

// Error handler
app.use((err, req, res, next) => {
  debug(`Internal Server Error: ${err.message}`);
  res.status(500).send('Internal Server Error');
});

app.listen(port, () => {
  debug(`Server is running on http://localhost:${port}`);
  console.log(`Server is running on http://localhost:${port}`);
});

module.exports = app;
