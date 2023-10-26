var express = require('express')
var app = express.Router()
const axios = require('axios'); // Importe a biblioteca axios

app.get('/', async (req, res) => {
  try {
    const url = 'http://localhost:3000/api/vinhos';

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

app.get('/Produto', (req, res) => {
  const year = 2023;
  const month = 0; // January
  const day = 15;
  const hour = 14;

  const filteredData = storeNames.map(storeName => ({
      type: "line",
      showInLegend: true,
      name: storeName,
      dataPoints: filterData(data, year, month, day, hour)
          .filter(loja => loja.StoreName === storeName)
          .map(loja => ({
              x: new Date(loja.Date),
              y: loja.Price
          }))
  }));

  res.render('chart', { chartData: filteredData });
});

app.get('/login', (req, res) => {
  res.render('login');
});

app.get('/removeProduto', (req, res) => {
  res.render('removeProduto');
});
module.exports = app;