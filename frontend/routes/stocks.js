const express = require('express');
const axios = require('axios');
const debug = require('debug')('app');
const router = express.Router();
const requireLogin = require('../middleware/auth');

router.get('/stocks', requireLogin, async (req, res) => {
  try {
    const response = await axios.get('http://localhost:5000/stocks');
    const stocks = response.data;
    res.render('stocks', { stocks, user: req.session.user });
  } catch (error) {
    res.status(500).send("Internal Server Error");
  }
});

module.exports = router;
