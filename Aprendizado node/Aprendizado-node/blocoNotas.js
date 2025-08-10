// Importa o módulo 'fs/promises' para ler e escrever arquivos de forma assíncrona
const fs = require('fs').promises;

// --- FUNÇÃO PARA ESCREVER NO ARQUIVO ---
// 'conteudo' é um PARÂMETRO. Ele vai receber um valor quando chamarmos a função.
async function escrever(conteudo) {
    // Aqui, 'conteudo' é usado como parte do texto que será gravado no arquivo.
    // fs.appendFile() adiciona o texto no final do arquivo 'mensagem.txt'.
    // '\n' adiciona uma quebra de linha.
    await fs.appendFile('mensagem.txt', conteudo + '\n', 'utf8');
}

// --- FUNÇÃO PARA LER O ARQUIVO ---
async function ler() {
    // 'dados' é uma VARIÁVEL LOCAL criada dentro da função.
    // Ela vai armazenar o resultado da leitura do arquivo 'mensagem.txt'.
    const dados = await fs.readFile('mensagem.txt', 'utf8');

    // Mostra o conteúdo do arquivo no console
    console.log(dados);
}

// --- EXECUTANDO AS FUNÇÕES ---

// Chamamos a função 'escrever', passando como valor para o parâmetro 'conteudo'
// a string "Anotação feita em ..." com a data/hora atual.
(async () => {
    await escrever("Anotação feita em " + new Date().toLocaleString());
    await ler(); // Lê e mostra no console o que foi escrito
})();
