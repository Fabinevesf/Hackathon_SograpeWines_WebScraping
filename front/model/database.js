const mysql = require('mysql');

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

module.exports = connection;