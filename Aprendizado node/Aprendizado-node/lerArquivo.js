// Importando o módulo interno 'fs' (file system)
//const fs = require('fs');

// Lendo o arquivo de forma assíncrona
//fs.readFile('mensagem.txt', 'utf8', (erro, dados) => {
    //if (erro) {
        //console.error("Erro ao ler o arquivo:", erro);
        //return;
    //}
    //console.log("Conteúdo do arquivo:");
    //console.log(dados);
//});

// Importa o módulo 'fs' com suporte a Promises
const fs = require('fs').promises;

async function lerArquivo() {
    try {
        // Aguarda a leitura do arquivo
        const dados = await fs.readFile('mensagem.txt', 'utf8');
        
        console.log("Conteúdo do arquivo:");
        console.log(dados);
    } catch (erro) {
        console.error("Erro ao ler o arquivo:", erro);
    }
}

// Chama a função
lerArquivo();
