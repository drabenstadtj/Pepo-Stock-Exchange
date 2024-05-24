const express = require('express');
const session = require('express-session');
const path = require('path');

const app = express();
const port = 3000;

app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'views'));

app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Configure session middleware
app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true
}));

// Middleware to check if the user is logged in
const requireLogin = (req, res, next) => {
  // Check if user is authenticated
  if (req.session && req.session.user) {
    next(); // Continue to the next middleware
  } else {
    res.redirect('/login'); // Redirect to the login page if not logged in
  }
};

// Apply the requireLogin middleware to all routes except the login route
app.use((req, res, next) => {
  if (req.path === '/login') {
    next(); // Allow access to the login route
  } else {
    requireLogin(req, res, next); // Apply requireLogin middleware to all other routes
  }
});

// Routes
app.get('/', (req, res) => {
  res.render('index');
});

// Login route
app.get('/login', (req, res) => {
  res.render('login');
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;

  // Check if username and password match
  if (username === 'jack' && password === 'pw') {
    // Set user session
    req.session.user = username;
    res.redirect('/'); // Redirect to the home page if login successful
  } else {
    res.send('Invalid username or password!');
  }
});

// About route
app.get('/about', (req, res) => {
    res.render('about');
});

// Dashboard route
app.get('/dashboard', (req, res) => {
    res.render('dashboard');
});

// Trade route
app.get('/trade', (req, res) => {
    res.render('trade');
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
