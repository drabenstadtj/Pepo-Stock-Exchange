const debug = require('debug')('app');

const requireLogin = (req, res, next) => {
  debug(`Checking if user is logged in: ${req.session.user}`);
  if (req.session && req.session.user) {
    next(); // User is logged in, proceed to the next middleware
  } else {
    debug('User not logged in, redirecting to /signin');
    res.redirect('/signin'); // Redirect to sign-in page if not logged in
  }
};

module.exports = requireLogin;
