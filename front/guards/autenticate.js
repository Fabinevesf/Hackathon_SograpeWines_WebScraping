var jwt = require("jsonwebtoken");
const supersecret = 'shhhhhhhh';
const cookie = require('cookie');

function autenticate(req, res, next) {
    const cookies = cookie.parse(req.headers.cookie || '');

    // Recuperar o token do cookie "token"
    const token = cookies.token;
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
