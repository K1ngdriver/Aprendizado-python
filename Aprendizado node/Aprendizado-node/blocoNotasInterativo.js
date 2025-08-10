const fs = require('fs').promises;
const readline = require('readline');

// Cria a interface para entrada de dados pelo terminal
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Função para perguntar algo e esperar a resposta do usuário
function perguntar(query) {
    return new Promise(resolve => rl.question(query, resolve));
}

async function escrever(conteudo) {
    try {
        await fs.appendFile('mensagem.txt', conteudo + '\n', 'utf8');
        console.log("✅ Texto adicionado com sucesso!");
    } catch (erro) {
        console.error("Erro ao escrever no arquivo:", erro);
    }
}

async function ler() {
    try {
        const dados = await fs.readFile('mensagem.txt', 'utf8');
        console.log("\n📄 Conteúdo do bloco de notas:");
        console.log(dados);
    } catch (erro) {
        console.error("Erro ao ler o arquivo:", erro);
    }
}

async function main() {
    // Pergunta o texto que o usuário quer adicionar
    const textoNovo = await perguntar("Digite sua anotação (ou apenas ENTER para sair): ");

    if (textoNovo.trim() === "") {
        console.log("Saindo do bloco de notas...");
        rl.close();
        return;
    }

    await escrever(textoNovo);
    await ler();

    // Chama main() de novo para permitir novas anotações até o usuário sair
    main();
}

// Inicia o programa
main();
