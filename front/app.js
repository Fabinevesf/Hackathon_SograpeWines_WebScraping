const express = require('express');
const mysql = require('mysql');
const ejs = require('ejs');
const bodyParser = require('body-parser');

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

const wineData = [{"vinho":{"EAN":"5601012001310","name":"Mateus Rosé Sparkling","capacity":750,"Brand":"Sograpes Vinhos","Subrand":"None"},"loja":[{"scrape_id":1,"EAN":"5601012001310","StoreName":"El Corte Ingles","HarvestYear":0,"Price":6.99,"Discount":0,"Currency":"€","Date":"2023-10-24T15:22:57.000Z","Location":"Portugal"},{"scrape_id":3,"EAN":"5601012001310","StoreName":"Continente","HarvestYear":0,"Price":6.99,"Discount":0,"Currency":"€","Date":"2023-10-24T15:30:38.000Z","Location":"Portugal"},{"scrape_id":4,"EAN":"5601012001310","StoreName":"El Corte Ingles","HarvestYear":0,"Price":6.99,"Discount":0,"Currency":"€","Date":"2023-10-24T15:30:40.000Z","Location":"Portugal"},{"scrape_id":7,"EAN":"5601012001310","StoreName":"El Corte Ingles","HarvestYear":0,"Price":6.99,"Discount":0,"Currency":"€","Date":"2023-10-24T15:32:50.000Z","Location":"Portugal"},{"scrape_id":9,"EAN":"5601012001310","StoreName":"El Corte Ingles","HarvestYear":0,"Price":6.99,"Discount":0,"Currency":"€","Date":"2023-10-24T15:33:26.000Z","Location":"Portugal"}]},{"vinho":{"EAN":"5601012011920","name":"Papa Figos","capacity":750,"Brand":"Casa Ferreirinha","Subrand":"Papa Figos"},"loja":[{"scrape_id":2,"EAN":"5601012011920","StoreName":"El Corte Ingles","HarvestYear":0,"Price":7.99,"Discount":0,"Currency":"€","Date":"2023-10-24T15:22:59.000Z","Location":"Portugal"},{"scrape_id":5,"EAN":"5601012011920","StoreName":"Continente","HarvestYear":0,"Price":7.99,"Discount":0,"Currency":"€","Date":"2023-10-24T15:30:55.000Z","Location":"Portugal"},{"scrape_id":6,"EAN":"5601012011920","StoreName":"El Corte Ingles","HarvestYear":0,"Price":7.99,"Discount":0,"Currency":"€","Date":"2023-10-24T15:30:56.000Z","Location":"Portugal"},{"scrape_id":8,"EAN":"5601012011920","StoreName":"El Corte Ingles","HarvestYear":0,"Price":7.99,"Discount":0,"Currency":"€","Date":"2023-10-24T15:32:52.000Z","Location":"Portugal"},{"scrape_id":10,"EAN":"5601012011920","StoreName":"El Corte Ingles","HarvestYear":0,"Price":7.99,"Discount":0,"Currency":"€","Date":"2023-10-24T15:33:41.000Z","Location":"Portugal"}]}];
app.get('/', (req, res) => {
    res.render('home', { wines: wineData });
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