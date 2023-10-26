const connection = require("../model/database")
const autenticate = require("../guards/autenticate")
var express = require('express')
var router = express.Router()
var jwt = require('jsonwebtoken')
var bcrypt = require('bcrypt')
const saltRounds = 10
const supersecret = 'shhhhhhhh';

const bodyParser = require('body-parser');
router.use(bodyParser.json());
router.use(bodyParser.urlencoded({ extended: true }));

router.post('/register', autenticate, async (req, res) => {
    const { username, password , name} = req.body
    console.log(username, password , name);

    try {
        const hash = await bcrypt.hash(password, saltRounds)
    
        const query = 'INSERT INTO logindb (username, password, fullname) VALUES (?, ?, ?)'
        connection.query(query, [username, hash, name], (err, results) => {
            if (err)
                res.send('Error');
            else
                res.send('Added');
        });

        //res.send({ message: 'Register successful' })
    } catch (err) {
        res.status(400).send({ message: err.message })
    }
  })

router.post('/login', async (req, res) => {
    const { username, password } = req.body
  
    try {
    const query = 'SELECT * FROM logindb WHERE username = ?'
        connection.query(query, [username], async (err, results) => {
//            res.send(results[0]);
            const user = results[0]
            if (user) {
                const user_id = user.id
        
                const correctPassword = await bcrypt.compare(password, user.password)
        
                if (!correctPassword) res.status(400).send({ message: 'Password errada'});

                var token = jwt.sign({ user_id }, supersecret)
                res.cookie('token', token, { httpOnly: true });
                res.redirect('/')
            } else {
                res.status(400).send({ message: 'User nao existe'});
            }
        });
    } catch (err) {
      res.status(400).send({ message: err.message })
    }
  })

  router.get('/logout', (req, res) => {
    res.clearCookie('token');
    res.redirect('/login'); // Substitua com a página desejada
  });

  module.exports = router;