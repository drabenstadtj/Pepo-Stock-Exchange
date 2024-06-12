const express = require('express');
const session = require('express-session');
const path = require('path');
const dotenv = require('dotenv');
const axios = require('axios');
const jwt = require('jsonwebtoken');
const { createProxyMiddleware } = require('http-proxy-middleware');
const morgan = require('morgan');

// Load environment variables from .env file
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const app = express();
const port = process.env.FRONTEND_PORT || 3000;
const backendPort = process.env.BACKEND_PORT || 5000;
const isProduction = process.env.CONFIG === 'production';

// Verify that SECRET_KEY and SESSION_SECRET are set
const secretKey = process.env.SECRET_KEY;
const sessionSecret = process.env.SESSION_SECRET;
const signupPasscode = process.env.SIGNUP_PASSCODE;

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
app.set('views', path.join(__dirname, './views'));

// Middleware to parse URL-encoded bodies and serve static files
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, './public')));

// Configure session middleware
app.use(session({
  secret: sessionSecret,
  resave: false,
  saveUninitialized: true,
  cookie: {
    httpOnly: true,
    secure: isProduction,
    sameSite: isProduction ? 'None' : 'Lax',
    maxAge: 24 * 60 * 60 * 1000  // Cookie expiration time
  }
}));

// Add request logging
app.use(morgan('combined'));

// Middleware to require login
const requireLogin = (req, res, next) => {
  if (req.session && req.session.token) {
    try {
      const decoded = jwt.verify(req.session.token, secretKey);
      req.user = decoded;
      next();
    } catch (err) {
      console.error('Token verification error:', err);
      res.redirect('/signin');
    }
  } else {
    res.redirect('/signin');
  }
};

// Middleware to attach token to headers
const attachToken = (req, res, next) => {
  if (req.session && req.session.token) {
    req.headers['Authorization'] = `Bearer ${req.session.token}`;
  }
  next();
};

// Helper function to get backend URL
const getBackendUrl = (endpoint) => {
  return `http://localhost:${backendPort}${endpoint}`;
};

// Routes
app.get('/signup', (req, res) => {
  res.render('signup', { user: req.session.user, isProduction });
});

app.post('/signup', async (req, res) => {
  const { username, password, passcode } = req.body;

  if (isProduction && passcode !== signupPasscode) {
    return res.render('signup', { error: 'Incorrect passcode', isProduction });
  }

  try {
    const response = await axios.post(getBackendUrl('/auth/register'), { username, password });
    if (response.data.message === 'User registered successfully') {
      req.session.user = username;
      req.session.token = response.data.token;
      res.redirect('/');
    } else {
      res.send('Signup failed!');
    }
  } catch (error) {
    console.error('Signup error:', error);
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
    const response = await axios.post(getBackendUrl('/auth/verify_credentials'), { username, password });
    if (response.data.message === 'Credentials verified') {
      req.session.user = username;
      req.session.token = response.data.token;
      req.session.save(err => {
        if (err) {
          res.redirect('/signin?error=Session error');
        } else {
          res.redirect('/');
        }
      });
    } else {
      res.redirect('/signin?error=Invalid username or password');
    }
  } catch (error) {
    console.error('Signin error:', error);
    res.redirect('/signin?error=Invalid username or password');
  }
});

app.get('/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      console.error('Logout error:', err);
      return res.redirect('/');
    }
    res.clearCookie('connect.sid');
    res.redirect('/signin');
  });
});

app.get('/', requireLogin, attachToken, (req, res) => {
  res.render('index', { user: req.session.user });
});

app.get('/leaderboard', requireLogin, attachToken, (req, res) => {
  res.render('leaderboard', { title: 'Leaderboard', user: req.session.user });
});

app.get('/about', requireLogin, attachToken, (req, res) => {
  res.render('about', { user: req.session.user });
});

app.get('/trade', requireLogin, attachToken, async (req, res) => {
  try {
    const token = req.session.token;
    const portfolioResponse = await axios.get(getBackendUrl('/portfolio/stocks'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const balanceResponse = await axios.get(getBackendUrl('/portfolio/balance'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const assetsValueResponse = await axios.get(getBackendUrl('/portfolio/assets_value'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    const portfolio = portfolioResponse.data;
    const balance = balanceResponse.data;
    const assets_value = assetsValueResponse.data;

    res.render('trade', { user: req.session.user, portfolio, balance, assets_value, token });
  } catch (error) {
    console.error('Trade fetch error:', error);
    res.status(500).send("Internal Server Error");
  }
});

app.get('/stocks', requireLogin, attachToken, async (req, res) => {
  try {
    const response = await axios.get(getBackendUrl('/stocks'));
    const stocks = response.data;
    const token = req.session.token;

    res.render('stocks', { stocks, user: req.session.user, token });
  } catch (error) {
    console.error('Stocks fetch error:', error);
    res.status(500).send("Internal Server Error");
  }
});

app.use((err, req, res, next) => {
  console.error('Internal Server Error:', err);
  res.status(500).send('Internal Server Error');
});

if (isProduction) {
  app.listen(port, () => {
    console.log(`Server is running in production mode on http://localhost:${port}`);
  });
} else {
  app.use('/api', createProxyMiddleware({ target: `http://localhost:${backendPort}`, changeOrigin: true }));
  app.listen(port, () => {
    console.log(`Server is running in development mode on http://localhost:${port}`);
  });
}
