const express = require('express');
const axios = require('axios');
const debug = require('debug')('app');
const router = express.Router();
const requireLogin = require('../middleware/auth');

router.get('/trade', requireLogin, async (req, res) => {
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

    res.render('trade', { user: req.session.user, user_id: user_id, portfolio, balance });
  } catch (error) {
    res.status(500).send("Internal Server Error");
  }
});

module.exports = router;
