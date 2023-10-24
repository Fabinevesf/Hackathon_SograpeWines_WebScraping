app.get('/vinhos', async (req, res) => {
    try {
      // Consulta na primeira tabela para obter a lista de vinhos
      const vinhos = await connection.query('SELECT EAN, Nome_vinho, capacidade, marca, submarca FROM primeira_tabela');
  
      const resultado = [];
  
      for (const vinho of vinhos) {
        // Para cada vinho, consulte a segunda tabela usando o EAN
        const dadosLoja = await connection.query('SELECT * FROM segunda_tabela WHERE EAN = ?', [vinho.EAN]);
  
        // Adicione os dados do vinho e da loja ao resultado
        resultado.push({
          vinho: vinho,
          loja: dadosLoja,
        });
      }
  
      res.json(resultado);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Ocorreu um erro ao buscar os dados.' });
    }
  });
  