const express = require('express');
const ejs = require('ejs');
const bodyParser = require('body-parser');
var createError = require("http-errors");


const app = express();
const port = process.env.PORT || 3000;

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

var routesRouter = require("./routes/route");
app.use('/', routesRouter);

var apiRouter = require("./routes/api");
app.use('/api/', apiRouter);

var usersRouter = require("./routes/user");
app.use('/user/', usersRouter);

app.use(function(req, res, next) {
    next(createError(404));
});

  function promisifyQuery(sql) {
    return new Promise((resolve, reject) => {
      connection.query(sql, (err, results) => {
        if (err) {
          reject(err);
        } else {
          resolve(results);
        }
      });
    });
  }


app.listen(port, () => {
    console.log(`Servidor rodando na porta ${port}`);
});