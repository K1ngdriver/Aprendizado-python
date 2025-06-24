import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from pathlib import Path
import os

class TextFrequencyAnalyzer:
    def __init__(self):
        self.texts = []
        self.word_frequencies = {}
        
    def add_text(self, text, source_name="Texto"):
        """Adiciona um texto à análise"""
        self.texts.append({
            'text': text,
            'source': source_name
        })
    
    def load_text_file(self, file_path, encoding='utf-8'):
        """Carrega texto de um arquivo"""
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                text = file.read()
                file_name = Path(file_path).stem
                self.add_text(text, file_name)
                print(f"Arquivo '{file_name}' carregado com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")
    
    def preprocess_text(self, text):
        """Preprocessa o texto (remove pontuação, converte para minúsculas)"""
        # Remove pontuação e caracteres especiais, mantém apenas letras e espaços
        text = re.sub(r'[^\w\s]', ' ', text)
        # Converte para minúsculas
        text = text.lower()
        # Remove espaços extras
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def analyze_frequency(self, target_words, case_sensitive=False):
        """
        Analisa a frequência das palavras especificadas
        
        Args:
            target_words: lista de palavras para analisar
            case_sensitive: se True, considera maiúsculas/minúsculas
        """
        if not case_sensitive:
            target_words = [word.lower() for word in target_words]
        
        self.word_frequencies = {word: [] for word in target_words}
        
        for text_data in self.texts:
            text = text_data['text']
            source = text_data['source']
            
            if not case_sensitive:
                processed_text = self.preprocess_text(text)
            else:
                processed_text = text
            
            words = processed_text.split()
            word_count = Counter(words)
            
            # Conta a frequência de cada palavra alvo
            for target_word in target_words:
                frequency = word_count.get(target_word, 0)
                self.word_frequencies[target_word].append({
                    'source': source,
                    'frequency': frequency
                })
        
        return self.word_frequencies
    
    def create_frequency_dataframe(self):
        """Cria um DataFrame com os resultados da análise"""
        data = []
        for word, freq_list in self.word_frequencies.items():
            for freq_data in freq_list:
                data.append({
                    'palavra': word,
                    'fonte': freq_data['source'],
                    'frequencia': freq_data['frequency']
                })
        
        return pd.DataFrame(data)
    
    def plot_frequency_bar(self, figsize=(12, 6), title="Frequência de Palavras"):
        """Cria gráfico de barras horizontal da frequência das palavras com a frequencia de cada palavra"""
        df = self.create_frequency_dataframe()
        
        plt.figure(figsize=figsize)
        
        if len(self.texts) == 1:
            # Se há apenas um texto, mostra frequência simples
            word_totals = df.groupby('palavra')['frequencia'].sum().sort_values(ascending=False)
            plt.barh(word_totals.index, word_totals.values)

            for index, value in enumerate(word_totals.values):
                plt.text(value, index, str(value), ha='left', va='center')

            plt.title(title)
            plt.xlabel('Palavras')
            plt.ylabel('Frequência')
            plt.xticks(rotation=45)
        else:
            # Se há múltiplos textos, mostra comparação
            pivot_df = df.pivot(index='palavra', columns='fonte', values='frequencia').fillna(0)
            pivot_df.plot(kind='bar', figsize=figsize)
            ax = pivot_df.plot(kind='bar', figsize=figsize)
            for container in ax.containers:
                for bar in container:
                    width = bar.get_width()
                    ax.text(width +0.1, bar.get_y() + bar.get_height()/2,
                            f'{int(width)}', ha='left', va='center', fontsize=9)
            plt.title(title)
            plt.xlabel('Palavras')
            plt.ylabel('Frequência')
            plt.xticks(rotation=45)
            plt.legend(title='Fonte', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.show()
    
    def plot_frequency_heatmap(self, figsize=(10, 6)):
        """Cria um heatmap da frequência das palavras (útil para múltiplos textos)"""
        if len(self.texts) <= 1:
            print("Heatmap requer múltiplos textos para comparação.")
            return
        
        df = self.create_frequency_dataframe()
        pivot_df = df.pivot(index='palavra', columns='fonte', values='frequencia').fillna(0)
        
        plt.figure(figsize=figsize)
        sns.heatmap(pivot_df, annot=True, cmap='YlOrRd', fmt='g')
        plt.title('Mapa de Calor - Frequência de Palavras por Fonte')
        plt.tight_layout()
        plt.show()
    
    def get_summary_stats(self):
        """Retorna estatísticas resumidas da análise"""
        df = self.create_frequency_dataframe()
        summary = df.groupby('palavra').agg({
            'frequencia': ['sum', 'mean', 'std', 'max', 'min']
        }).round(2)
        
        summary.columns = ['Total', 'Média', 'Desvio Padrão', 'Máximo', 'Mínimo']
        return summary

# Exemplo de uso
if __name__ == "__main__":
    # Criar instância do analisador
    analyzer = TextFrequencyAnalyzer()
    
    caminho_corpus = os.path.expanduser("~/Downloads/corpus.txt")

    try:
        analyzer.load_text_file(caminho_corpus)
        print(f"Corpus carregado com sucesso de: {caminho_corpus}")
    except FileNotFoundError:
        print(f"Arquivo não encontrado em: {caminho_corpus}")
        print("Verifique se o arquivo existe e o caminho está correto.")
        
        # Mostrar caminhos possíveis para ajudar
        print("\nTente um destes caminhos:")
        print("Windows: C:\\Users\\SeuUsuario\\Downloads\\corpus.txt")
        print("Linux/Mac: /home/seuusuario/Downloads/corpus.txt")
        print("Ou use: os.path.expanduser('~/Downloads/corpus.txt')")
    
    # Palavras que queremos analisar
    palavras_alvo = ["architecture", "security", "privacy"]
    
    # Realizar análise
    frequencias = analyzer.analyze_frequency(palavras_alvo)
    
    # Mostrar resultados
    print("=== ANÁLISE DE FREQUÊNCIA DE PALAVRAS ===\n")
    
    df_results = analyzer.create_frequency_dataframe()
    print("DataFrame com resultados:")
    print(df_results)
    print("\n")
    
    print("Estatísticas resumidas:")
    print(analyzer.get_summary_stats())
    print("\n")
    
    # Criar visualizações
    analyzer.plot_frequency_bar(title="Frequência das Palavras-Chave")
    analyzer.plot_frequency_heatmap()
    
    # Exemplo de como carregar arquivos de texto
    # analyzer.load_text_file("caminho/para/seu/arquivo.txt")
    
    print("Para usar com seus próprios arquivos:")
    print("1. Use analyzer.load_text_file('caminho/arquivo.txt')")
    print("2. Ou use analyzer.add_text(seu_texto, 'nome_fonte')")
    print("3. Execute analyzer.analyze_frequency(lista_palavras)")
    print("4. Visualize com analyzer.plot_frequency_bar() ou plot_frequency_heatmap()")