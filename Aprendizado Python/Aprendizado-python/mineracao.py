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
    
    def add_pasted_text(self, text, source_name="Texto Colado"):
        """
        Adiciona texto colado diretamente
        
        Args:
            text: o texto completo colado
            source_name: nome para identificar este texto
        """
        if not text.strip():
            print("Erro: Texto vazio fornecido!")
            return False
            
        self.add_text(text.strip(), source_name)
        word_count = len(text.split())
        char_count = len(text)
        print(f"✓ Texto '{source_name}' adicionado com sucesso!")
        print(f"  - Caracteres: {char_count:,}")
        print(f"  - Palavras: {word_count:,}")
        return True
    
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
    
    def interactive_text_input(self):
        """Método interativo para colar texto"""
        print("\n=== ADICIONAR TEXTO COLADO ===")
        print("Cole seu texto abaixo (pressione Enter duas vezes para finalizar):")
        print("Ou digite 'quit' para cancelar\n")
        
        lines = []
        empty_line_count = 0
        
        while True:
            try:
                line = input()
                if line.lower().strip() == 'quit':
                    print("Operação cancelada.")
                    return False
                    
                if line.strip() == '':
                    empty_line_count += 1
                    if empty_line_count >= 2:
                        break
                else:
                    empty_line_count = 0
                    
                lines.append(line)
            except KeyboardInterrupt:
                print("\nOperação cancelada.")
                return False
        
        # Remove linhas vazias do final
        while lines and lines[-1].strip() == '':
            lines.pop()
            
        if not lines:
            print("Nenhum texto foi fornecido.")
            return False
            
        text = '\n'.join(lines)
        
        # Pedir nome para o texto
        source_name = input("\nDigite um nome para este texto (ou pressione Enter para usar 'Texto Colado'): ").strip()
        if not source_name:
            source_name = "Texto Colado"
            
        return self.add_pasted_text(text, source_name)
    
    def analyze_frequency(self, target_words, case_sensitive=False):
        """
        Analisa a frequência das palavras especificadas
        
        Args:
            target_words: lista de palavras para analisar
            case_sensitive: se True, considera maiúsculas/minúsculas
        """
        if not self.texts:
            print("Erro: Nenhum texto foi adicionado para análise!")
            return {}
            
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
        if not self.word_frequencies:
            print("Erro: Execute analyze_frequency() primeiro!")
            return pd.DataFrame()
            
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
        """Cria gráfico de barras da frequência das palavras"""
        df = self.create_frequency_dataframe()
        
        if df.empty:
            print("Erro: Nenhum dado para plotar!")
            return
            
        plt.figure(figsize=figsize)
        
        if len(self.texts) == 1:
            # Se há apenas um texto, mostra frequência simples
            word_totals = df.groupby('palavra')['frequencia'].sum().sort_values(ascending=False)
            bars = plt.barh(word_totals.index, word_totals.values)

            # Adiciona valores nas barras
            for i, (bar, value) in enumerate(zip(bars, word_totals.values)):
                plt.text(value + 0.1, i, str(value), ha='left', va='center')

            plt.title(title)
            plt.xlabel('Frequência')
            plt.ylabel('Palavras')
        else:
            # Se há múltiplos textos, mostra comparação
            pivot_df = df.pivot(index='palavra', columns='fonte', values='frequencia').fillna(0)
            ax = pivot_df.plot(kind='bar', figsize=figsize)
            
            # Adiciona valores nas barras
            for container in ax.containers:
                ax.bar_label(container, fmt='%d')
                
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
        if df.empty:
            print("Erro: Nenhum dado para plotar!")
            return
            
        pivot_df = df.pivot(index='palavra', columns='fonte', values='frequencia').fillna(0)
        
        plt.figure(figsize=figsize)
        sns.heatmap(pivot_df, annot=True, cmap='YlOrRd', fmt='g')
        plt.title('Mapa de Calor - Frequência de Palavras por Fonte')
        plt.tight_layout()
        plt.show()
    
    def get_summary_stats(self):
        """Retorna estatísticas resumidas da análise"""
        df = self.create_frequency_dataframe()
        if df.empty:
            print("Erro: Nenhum dado para análise!")
            return pd.DataFrame()
            
        summary = df.groupby('palavra').agg({
            'frequencia': ['sum', 'mean', 'std', 'max', 'min']
        }).round(2)
        
        summary.columns = ['Total', 'Média', 'Desvio Padrão', 'Máximo', 'Mínimo']
        return summary
    
    def show_text_info(self):
        """Mostra informações sobre os textos carregados"""
        if not self.texts:
            print("Nenhum texto carregado.")
            return
            
        print("\n=== TEXTOS CARREGADOS ===")
        for i, text_data in enumerate(self.texts, 1):
            text = text_data['text']
            source = text_data['source']
            word_count = len(text.split())
            char_count = len(text)
            
            print(f"{i}. Fonte: {source}")
            print(f"   Caracteres: {char_count:,}")
            print(f"   Palavras: {word_count:,}")
            print(f"   Prévia: {text[:100]}...")
            print()

def main():
    """Função principal com interface interativa"""
    print("=== ANALISADOR DE FREQUÊNCIA DE PALAVRAS ===\n")
    
    analyzer = TextFrequencyAnalyzer()
    
    while True:
        print("\nEscolha uma opção:")
        print("1. Colar texto diretamente")
        print("2. Carregar arquivo de texto")
        print("3. Ver textos carregados")
        print("4. Analisar frequência de palavras")
        print("5. Sair")
        
        choice = input("\nDigite sua escolha (1-5): ").strip()
        
        if choice == '1':
            analyzer.interactive_text_input()
            
        elif choice == '2':
            file_path = input("Digite o caminho do arquivo: ").strip()
            if file_path:
                analyzer.load_text_file(file_path)
                
        elif choice == '3':
            analyzer.show_text_info()
            
        elif choice == '4':
            if not analyzer.texts:
                print("Erro: Adicione pelo menos um texto primeiro!")
                continue
                
            words_input = input("Digite as palavras para analisar (separadas por vírgula): ").strip()
            if not words_input:
                print("Nenhuma palavra fornecida!")
                continue
                
            target_words = [word.strip() for word in words_input.split(',')]
            
            print(f"\nAnalisando palavras: {target_words}")
            frequencies = analyzer.analyze_frequency(target_words)
            
            if frequencies:
                print("\n=== RESULTADOS ===")
                df_results = analyzer.create_frequency_dataframe()
                print(df_results)
                
                print("\n=== ESTATÍSTICAS ===")
                print(analyzer.get_summary_stats())
                
                # Perguntar se quer visualizar
                show_plot = input("\nDeseja ver os gráficos? (s/n): ").strip().lower()
                if show_plot in ['s', 'sim', 'yes', 'y']:
                    analyzer.plot_frequency_bar()
                    if len(analyzer.texts) > 1:
                        analyzer.plot_frequency_heatmap()
                        
        elif choice == '5':
            print("Saindo...")
            break
            
        else:
            print("Opção inválida! Tente novamente.")

# Exemplo de uso direto (sem interface interativa)
if __name__ == "__main__":
    # Descomente a linha abaixo para usar a interface interativa
    main()
    
    # Ou use diretamente assim:
    # analyzer = TextFrequencyAnalyzer()
    # 
    # # Exemplo de uso direto colando texto
    # meu_texto = """
    # Cole seu texto aqui...
    # """
    # analyzer.add_pasted_text(meu_texto, "Meu Corpus")
    # 
    # # Analisar palavras
    # palavras = ["palavra1", "palavra2", "palavra3"]
    # analyzer.analyze_frequency(palavras)
    # 
    # # Ver resultados
    # print(analyzer.create_frequency_dataframe())
    # analyzer.plot_frequency_bar()