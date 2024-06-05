const express = require('express');
const axios = require('axios');
const debug = require('debug')('app');
const router = express.Router();

router.get('/signup', (req, res) => {
  res.render('signup', { user: req.session.user });
});

router.post('/signup', async (req, res) => {
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
    res.status(500).send('Signup failed!');
  }
});

router.get('/signin', (req, res) => {
  const error = req.query.error;
  res.render('signin', { error, user: req.session.user });
});

router.post('/signin', async (req, res) => {
  const { username, password } = req.body;
  try {
    const response = await axios.post('http://localhost:5000/auth/verify_credentials', { username, password });
    if (response.data.message === 'Credentials verified') {
      req.session.user = username;
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
    res.redirect('/signin?error=Invalid username or password');
  }
});

router.get('/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      return res.redirect('/');
    }
    res.clearCookie('connect.sid');
    res.redirect('/signin');
  });
});

module.exports = router;
