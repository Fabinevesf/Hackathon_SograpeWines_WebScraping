var jwt = require("jsonwebtoken");
const supersecret = 'shhhhhhhh';

function autenticate(req, res, next) {
  const token = '';

  if (!token) {
    res.redirect('/login');
  } else {
    jwt.verify(token, supersecret, function (err, decoded) {
      if (err)     res.redirect('/login');      //.status(401).send({ message: err.message });
      else {
        //everything is awesome
        req.user_id = decoded.user_id;
        next();
      }
    });
  }
}

module.exports = autenticate;
