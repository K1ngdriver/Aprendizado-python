// Importa o módulo 'fs' com suporte a Promises
const fs = require('fs').promises;

async function escreverArquivo() {
    try {
        const conteudo = "Esse texto foi escrito usando Node.js com async/await!";
        
        // Escreve no arquivo (se não existir, cria)
        await fs.writeFile('mensagem.txt', conteudo, 'utf8');
        
        console.log("Arquivo criado/atualizado com sucesso!");
    } catch (erro) {
        console.error("Erro ao escrever no arquivo:", erro);
    }
}

// Chama a função
escreverArquivo();
