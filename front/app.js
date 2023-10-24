const express = require('express');
const mysql = require('mysql');
const ejs = require('ejs');
const bodyParser = require('body-parser');
const axios = require('axios'); // Importe a biblioteca axios

const app = express();
const port = process.env.PORT || 3000;

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));

const connection = mysql.createConnection({
    host: '34.175.219.22',
    user: 'root',
    password: 'root',
    database: 'wines'
});

connection.connect((err) => {
    if (err) {
        console.error('Erro ao conectar ao banco de dados: ' + err.stack);
        return;
    }
    console.log('Conectado como ID ' + connection.threadId);
});

app.get('/', async (req, res) => {
  try {
    const url = 'http://localhost:3000/vinhos';

    // Faz a solicitação GET usando axios
    const response = await axios.get(url);

    // Envie a resposta do site externo de volta como a resposta do seu servidor
    res.render('home', { wines: response.data }); // Renderize a página EJS com os dados da resposta
  } catch (error) {
    console.error('Erro ao fazer a solicitação GET:', error);
    res.status(500).send('Erro ao fazer a solicitação GET.');
  }
});

app.get('/addProduto', (req, res) => {
    res.render('addProduto');
});

app.get('/removeProduto', (req, res) => {
  res.render('removeProduto');
});

app.post('/submit', (req, res) => {
    const dados = {
        nomeVinho: req.body.nomeVinho,
        capacidade: req.body.capacidade,
        ean: req.body.ean,
        marca: req.body.marca,
        submarca: req.body.submarca
    };

    const query = 'INSERT INTO wines (name, capacity, EAN, Brand, Subrand) VALUES (?, ?, ?, ?, ?)';
    connection.query(query, [dados.nomeVinho, dados.capacidade, dados.ean, dados.marca, dados.submarca], (err, results) => {
        if (err) throw err;
        console.log('Dados inseridos com sucesso. ID do registro: ' + results.insertId);
        res.send('Dados recebidos com sucesso e inseridos no banco de dados!');
    });
});

app.post('/remove', (req, res) => {
    const dados = {
        ean: req.body.ean
    };

    const query = 'DELETE FROM wines WHERE EAN = ?';
    connection.query(query, [dados.ean], (err, results) => {
        if (err) throw err;
        console.log('Dados removidos com sucesso. ID do registro: ' + results.insertId);
        res.send('Dados removidos com sucesso!');
    });
});

app.get('/vinhos', async (req, res) => {
    try {
      const resultado = [];
  
      const vinhos = await promisifyQuery('SELECT EAN, name, capacity, Brand, Subrand FROM wines');
  
      for (const vinho of vinhos) {
        const dadosLoja = await promisifyQuery(`SELECT * FROM scrape WHERE EAN = ${vinho.EAN}`);
        resultado.push({
          vinho: vinho,
          loja: dadosLoja,
        });
      }
  
      res.status(200).json(resultado);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Ocorreu um erro ao buscar os dados.' });
    }
  });
  
  app.get('/vinho', async (req, res) => {
    try {
      const resultado = [];
  
      const EAN = req.query.EAN;

      const dadosLoja = await promisifyQuery(`SELECT * FROM scrape WHERE EAN = ${EAN}`);
      resultado.push({
        lojas: dadosLoja,
      });
      const vinho = await promisifyQuery(`SELECT * FROM wines WHERE EAN = ${EAN}`);;
      res.render("Produto",{resultado, vinho});
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Ocorreu um erro ao buscar os dados.' });
    }
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