const express = require('express');
const session = require('express-session');
const debug = require('debug')('app');
const axios = require('axios');
const path = require('path');
const dotenv = require('dotenv');
const jwt = require('jsonwebtoken');

// Load environment variables from .env file located in the parent directory
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const app = express();
const port = process.env.PORT || 3000;

// Verify that SECRET_KEY and SESSION_SECRET are set
const secretKey = process.env.SECRET_KEY;
const sessionSecret = process.env.SESSION_SECRET;

if (!secretKey) {
  console.error('Error: SECRET_KEY is not set in the environment variables.');
  process.exit(1);
}

if (!sessionSecret) {
  console.error('Error: SESSION_SECRET is not set in the environment variables.');
  process.exit(1);
}

// Set the view engine to Pug and specify the views directory
app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'views'));

// Middleware to parse URL-encoded bodies and serve static files
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Configure session middleware
app.use(session({
  secret: sessionSecret, // Use SESSION_SECRET from .env file
  resave: false,
  saveUninitialized: true,
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production', // Set to true in production environment
    maxAge: 24 * 60 * 60 * 1000  // Cookie expiration time
  }
}));


// Middleware to require login
const requireLogin = (req, res, next) => {
  debug(`Checking if user is logged in: ${req.session.user}`);
  if (req.session && req.session.token) {
    try {
      const decoded = jwt.verify(req.session.token, secretKey);
      req.user = decoded;
      next(); // User is logged in, proceed to the next middleware
    } catch (err) {
      debug(`Token verification failed: ${err.message}`);
      res.redirect('/signin'); // Redirect to sign-in page if token is invalid
    }
  } else {
    debug('User not logged in, redirecting to /signin');
    res.redirect('/signin'); // Redirect to sign-in page if not logged in
  }
};

// Middleware to attach token to headers
const attachToken = (req, res, next) => {
  if (req.session && req.session.token) {
    req.headers['Authorization'] = `Bearer ${req.session.token}`;
  }
  next();
};

// Routes

// Render the sign-up page
app.get('/signup', (req, res) => {
  res.render('signup', { user: req.session.user });
});

// Handle sign-up form submission
app.post('/signup', async (req, res) => {
  const { username, password } = req.body;
  try {
    const response = await axios.post('http://localhost:5000/auth/register', { username, password });
    if (response.data.message === 'User registered successfully') {
      req.session.user = username; // Set the session user
      req.session.token = response.data.token; // Set the session token
      debug(`User ${username} registered successfully`);
      res.redirect('/'); // Redirect to home page
    } else {
      debug(`Signup failed for user ${username}: ${response.data.message}`);
      res.send('Signup failed!');
    }
  } catch (error) {
    debug(`Signup error for user ${username}: ${error.message}`);
    res.status(500).send('Signup failed!');
  }
});

// Render the sign-in page
app.get('/signin', (req, res) => {
  const error = req.query.error;
  res.render('signin', { error, user: req.session.user });
});

// Handle sign-in form submission
app.post('/signin', async (req, res) => {
  const { username, password } = req.body;
  try {
    debug(`Received signin request for user: ${username}`);
    
    const response = await axios.post('http://localhost:5000/auth/verify_credentials', { username, password });
    if (response.data.message === 'Credentials verified') {
      req.session.user = username; // Set the session user
      req.session.token = response.data.token; // Set the session token
      debug(`User ${username} signed in successfully`);
      req.session.save(err => {
        if (err) {
          debug(`Session save error: ${err.message}`);
          res.redirect('/signin?error=Session error');
        } else {
          res.redirect('/'); // Redirect to home page
        }
      });
    } else {
      debug(`Sign in failed for user ${username}: Invalid credentials`);
      res.redirect('/signin?error=Invalid username or password');
    }
  } catch (error) {
    debug(`Sign in error for user ${username}: ${error.message}`);
    res.redirect('/signin?error=Invalid username or password');
  }
});

// Handle user logout
app.get('/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      debug(`Logout error: ${err.message}`);
      return res.redirect('/');
    }
    res.clearCookie('connect.sid'); // Clear the session cookie
    debug(`User logged out successfully`);
    res.redirect('/signin'); // Redirect to sign-in page
  });
});

// Render the home page
app.get('/', requireLogin, attachToken, (req, res) => {
  debug(`Rendering home page for user ${req.session.user}`);
  res.render('index', { user: req.session.user });
});

// Route to serve the leaderboard view
app.get('/leaderboard', requireLogin, attachToken, (req, res) => {
  res.render('leaderboard', { title: 'Leaderboard', user: req.session.user  });
});

// Render the about page
app.get('/about', requireLogin, attachToken, (req, res) => {
  debug(`Rendering about page for user ${req.session.user}`);
  res.render('about', { user: req.session.user });
});

// Render the trade page with user's portfolio and balance
app.get('/trade', requireLogin, attachToken, async (req, res) => {
  try {
    const token = req.session.token;  // Use the token stored in the session

    const portfolioResponse = await axios.get('http://localhost:5000/portfolio/stocks', {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    const balanceResponse = await axios.get('http://localhost:5000/portfolio/balance', {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    const portfolio = portfolioResponse.data;
    const balance = balanceResponse.data;

    debug(`Fetched portfolio and balance for user ${req.session.user}`);
    res.render('trade', { user: req.session.user, portfolio, balance, token });
  } catch (error) {
    debug(`Error fetching portfolio for user ${req.session.user}: ${error.message}`);
    res.status(500).send("Internal Server Error");
  }
});

// Render the stocks page with available stocks
app.get('/stocks', requireLogin, attachToken, async (req, res) => {
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

// General error handler middleware
app.use((err, req, res, next) => {
  debug(`Internal Server Error: ${err.message}`);
  console.error(err.stack); // Log the stack trace to the console
  res.status(500).send('Internal Server Error');
});

// Start the server
app.listen(port, () => {
  debug(`Server is running on http://localhost:${port}`);
  console.log(`Server is running on http://localhost:${port}`);
});

module.exports = app;
