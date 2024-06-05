const express = require('express');
const router = express.Router();
const requireLogin = require('../middleware/auth');

router.get('/', requireLogin, (req, res) => {
  res.render('index', { user: req.session.user });
});

router.get('/about', requireLogin, (req, res) => {
  res.render('about', { user: req.session.user });
});

module.exports = router;
