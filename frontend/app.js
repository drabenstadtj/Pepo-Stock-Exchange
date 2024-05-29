const express = require('express');
const session = require('express-session');
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
  cookie: { secure: false, maxAge: 60000 } // Set secure to true if using HTTPS
}));

// Middleware to check if the user is logged in
const requireLogin = (req, res, next) => {
  if (req.session && req.session.user) {
    next();
  } else {
    res.redirect('/signin');
  }
};

app.get('/signup', (req, res) => {
  res.render('signup', { user: req.session.user });
});

app.post('/signup', async (req, res) => {
  const { username, password } = req.body;
  try {
    const response = await axios.post('http://localhost:5000/auth/register', { username, password });
    if (response.data.message === 'User registered successfully') {
      req.session.user = username;
      res.redirect('/');
    } else {
      res.send('Signup failed!');
    }
  } catch (error) {
    res.send('Signup failed!');
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
      res.redirect('/');
    } else {
      res.redirect('/signin?error=Invalid username or password');
    }
  } catch (error) {
    res.redirect('/signin?error=Invalid username or password');
  }
});

app.get('/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      return res.redirect('/');
    }
    res.clearCookie('connect.sid');
    res.redirect('/signin');
  });
});

// Routes
app.get('/', requireLogin, (req, res) => {
  res.render('index', { user: req.session.user });
});

app.get('/about', requireLogin, (req, res) => {
  res.render('about', { user: req.session.user });
});

app.get('/dashboard', requireLogin, (req, res) => {
  res.render('dashboard', { user: req.session.user });
});

app.get('/trade', requireLogin, (req, res) => {
  res.render('trade', { user: req.session.user });
});

// Route to fetch and display stocks from Flask backend
app.get('/stocks', requireLogin, async (req, res) => {
  try {
    const response = await axios.get('http://localhost:5000/stocks'); // Update the URL if necessary
    const stocks = response.data;

    res.render('stocks', { stocks, user: req.session.user });
  } catch (error) {
    console.error("Error fetching stocks: ", error);
    res.status(500).send("Internal Server Error");
  }
});

// Catch 404 and forward to error handler
app.use((req, res, next) => {
  res.status(404).send('Page not found');
});

// Error handler
app.use((err, req, res, next) => {
  res.status(500).send('Internal Server Error');
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

module.exports = app;
