import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from pathlib import Path
import os
import glob

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
            with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
                text = file.read()
                file_name = Path(file_path).stem
                self.add_text(text, file_name)
                print(f"✓ Arquivo '{file_name}' carregado com sucesso!")
        except Exception as e:
            print(f"✗ Erro ao carregar arquivo: {e}")
    
    def load_folder(self, folder_path, file_extensions=None, encoding='utf-8'):
        """
        Carrega todos os arquivos de texto de uma pasta
        
        Args:
            folder_path: caminho para a pasta
            file_extensions: lista de extensões (ex: ['.txt', '.md']) ou None para todas
            encoding: codificação dos arquivos
        """
        if file_extensions is None:
            file_extensions = ['.txt', '.md', '.doc', '.docx']
        
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            print(f"✗ Erro: Pasta não encontrada: {folder_path}")
            return 0
        
        files_loaded = 0
        
        # Procurar por todos os tipos de arquivo
        for ext in file_extensions:
            pattern = folder_path / f"*{ext}"
            files = glob.glob(str(pattern))
            
            for file_path in files:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
                        text = file.read()
                        if text.strip():  # Só adiciona se não estiver vazio
                            file_name = Path(file_path).stem
                            self.add_text(text, file_name)
                            files_loaded += 1
                            print(f"✓ Arquivo carregado: {file_name}")
                except Exception as e:
                    print(f"✗ Erro ao carregar {file_path}: {e}")
        
        if files_loaded == 0:
            print(f"✗ Nenhum arquivo encontrado em: {folder_path}")
            print(f"Extensões procuradas: {file_extensions}")
        else:
            print(f"\n✅ Total de arquivos carregados: {files_loaded}")
        
        return files_loaded
    
    def load_all_files_from_folder(self, folder_path, encoding='utf-8'):
        """
        Carrega TODOS os arquivos de uma pasta, independente da extensão
        """
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            print(f"✗ Erro: Pasta não encontrada: {folder_path}")
            return 0
        
        files_loaded = 0
        
        # Pegar todos os arquivos da pasta
        all_files = [f for f in folder_path.iterdir() if f.is_file()]
        
        for file_path in all_files:
            try:
                # Tentar ler como texto
                with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
                    text = file.read()
                    if text.strip():  # Só adiciona se não estiver vazio
                        file_name = file_path.stem
                        self.add_text(text, file_name)
                        files_loaded += 1
                        print(f"✓ Arquivo carregado: {file_name} ({file_path.suffix})")
            except Exception as e:
                print(f"✗ Erro ao carregar {file_path.name}: {e}")
        
        if files_loaded == 0:
            print(f"✗ Nenhum arquivo de texto encontrado em: {folder_path}")
        else:
            print(f"\n✅ Total de arquivos carregados: {files_loaded}")
        
        return files_loaded
    
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
    
    def analyze_individual_files(self, target_words, case_sensitive=False):
        """
        Analisa cada arquivo individualmente e retorna resultados detalhados
        """
        if not case_sensitive:
            target_words = [word.lower() for word in target_words]
        
        individual_results = {}
        
        for text_data in self.texts:
            text = text_data['text']
            source = text_data['source']
            
            if not case_sensitive:
                processed_text = self.preprocess_text(text)
            else:
                processed_text = text
            
            words = processed_text.split()
            word_count = Counter(words)
            total_words = len(words)
            
            # Resultados para este arquivo
            file_results = {
                'total_palavras': total_words,
                'palavras_encontradas': {},
                'percentuais': {}
            }
            
            for target_word in target_words:
                frequency = word_count.get(target_word, 0)
                percentage = (frequency / total_words * 100) if total_words > 0 else 0
                
                file_results['palavras_encontradas'][target_word] = frequency
                file_results['percentuais'][target_word] = round(percentage, 2)
            
            individual_results[source] = file_results
        
        return individual_results
    
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
    
    def plot_frequency_bar(self, figsize=(12, 6), title="Frequência de Palavras", horizontal=True):
        """Cria gráfico de barras da frequência das palavras com valores exibidos"""
        df = self.create_frequency_dataframe()
        
        plt.figure(figsize=figsize)
        
        if len(self.texts) == 1:
            # Se há apenas um texto, mostra frequência simples
            word_totals = df.groupby('palavra')['frequencia'].sum().sort_values(ascending=False)
            
            if horizontal:
                bars = plt.barh(word_totals.index, word_totals.values)
                # Adicionar valores nas barras
                for bar, value in zip(bars, word_totals.values):
                    plt.text(value + 0.1, bar.get_y() + bar.get_height()/2, 
                            str(value), ha='left', va='center', fontweight='bold')
                plt.xlabel('Frequência')
                plt.ylabel('Palavras')
            else:
                bars = plt.bar(word_totals.index, word_totals.values)
                # Adicionar valores nas barras
                for bar, value in zip(bars, word_totals.values):
                    plt.text(bar.get_x() + bar.get_width()/2, value + 0.1, 
                            str(value), ha='center', va='bottom', fontweight='bold')
                plt.xlabel('Palavras')
                plt.ylabel('Frequência')
                plt.xticks(rotation=45)
            
            plt.title(title, fontsize=14, fontweight='bold')
        else:
            # Se há múltiplos textos, mostra comparação
            pivot_df = df.pivot(index='palavra', columns='fonte', values='frequencia').fillna(0)
            
            if horizontal:
                ax = pivot_df.plot(kind='barh', figsize=figsize)
                # Adicionar valores nas barras
                for container in ax.containers:
                    ax.bar_label(container, fmt='%g', padding=3)
                plt.xlabel('Frequência')
                plt.ylabel('Palavras')
            else:
                ax = pivot_df.plot(kind='bar', figsize=figsize)
                # Adicionar valores nas barras
                for container in ax.containers:
                    ax.bar_label(container, fmt='%g', padding=3)
                plt.xlabel('Palavras')
                plt.ylabel('Frequência')
                plt.xticks(rotation=45)
            
            plt.title(title, fontsize=14, fontweight='bold')
            plt.legend(title='Fonte', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.show()
    
    def plot_individual_comparison(self, target_words, case_sensitive=False, figsize=(15, 8)):
        """Cria gráfico comparando palavras entre diferentes arquivos"""
        if len(self.texts) <= 1:
            print("Comparação individual requer múltiplos textos.")
            return
            
        individual_results = self.analyze_individual_files(target_words, case_sensitive)
        
        # Preparar dados para o gráfico
        data_for_plot = []
        for arquivo, dados in individual_results.items():
            for palavra in target_words:
                freq = dados['palavras_encontradas'].get(palavra, 0)
                data_for_plot.append({
                    'Arquivo': arquivo,
                    'Palavra': palavra,
                    'Frequência': freq
                })
        
        df_plot = pd.DataFrame(data_for_plot)
        
        # Criar gráfico
        plt.figure(figsize=figsize)
        
        # Gráfico de barras agrupadas
        pivot_df = df_plot.pivot(index='Arquivo', columns='Palavra', values='Frequência').fillna(0)
        ax = pivot_df.plot(kind='bar', figsize=figsize, width=0.8)
        
        # Adicionar valores nas barras
        for container in ax.containers:
            ax.bar_label(container, fmt='%g', padding=3)
        
        plt.title('Frequência de Palavras por Arquivo', fontsize=16, fontweight='bold')
        plt.xlabel('Arquivos', fontsize=12)
        plt.ylabel('Frequência', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Palavras', bbox_to_anchor=(1.05, 1), loc='upper left')
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
        sns.heatmap(pivot_df, annot=True, cmap='YlOrRd', fmt='g', cbar_kws={'label': 'Frequência'})
        plt.title('Mapa de Calor - Frequência de Palavras por Fonte', fontsize=14, fontweight='bold')
        plt.xlabel('Fonte', fontsize=12)
        plt.ylabel('Palavras', fontsize=12)
        plt.tight_layout()
        plt.show()
    
    def create_detailed_report(self, target_words, case_sensitive=False):
        """Cria relatório detalhado da análise individual"""
        individual_results = self.analyze_individual_files(target_words, case_sensitive)
        
        print("=" * 80)
        print("RELATÓRIO DETALHADO - ANÁLISE POR ARQUIVO")
        print("=" * 80)
        
        for arquivo, dados in individual_results.items():
            print(f"\n📄 ARQUIVO: {arquivo}")
            print(f"   Total de palavras: {dados['total_palavras']}")
            print(f"   Palavras analisadas:")
            
            for palavra in target_words:
                freq = dados['palavras_encontradas'].get(palavra, 0)
                perc = dados['percentuais'].get(palavra, 0)
                print(f"   • {palavra}: {freq} ocorrências ({perc}%)")
        
        return individual_results
    
    def export_results_to_csv(self, target_words, filename="resultados_mineracao.csv", case_sensitive=False):
        """Exporta resultados para CSV"""
        if len(self.texts) > 1:
            individual_results = self.analyze_individual_files(target_words, case_sensitive)
            
            # Preparar dados para CSV
            data_for_csv = []
            for arquivo, dados in individual_results.items():
                row = {'Arquivo': arquivo, 'Total_Palavras': dados['total_palavras']}
                
                for palavra in target_words:
                    freq = dados['palavras_encontradas'].get(palavra, 0)
                    perc = dados['percentuais'].get(palavra, 0)
                    row[f'{palavra}_Frequencia'] = freq
                    row[f'{palavra}_Percentual'] = perc
                
                data_for_csv.append(row)
            
            df_csv = pd.DataFrame(data_for_csv)
        else:
            # Para arquivo único, usar o DataFrame básico
            df_csv = self.create_frequency_dataframe()
        
        df_csv.to_csv(filename, index=False, encoding='utf-8')
        print(f"✓ Resultados exportados para: {filename}")
        return df_csv
    
    def get_summary_stats(self):
        """Retorna estatísticas resumidas da análise"""
        df = self.create_frequency_dataframe()
        summary = df.groupby('palavra').agg({
            'frequencia': ['sum', 'mean', 'std', 'max', 'min']
        }).round(2)
        
        summary.columns = ['Total', 'Média', 'Desvio Padrão', 'Máximo', 'Mínimo']
        return summary
    
    def interactive_menu(self):
        """Menu interativo para escolher o tipo de análise"""
        print("\n" + "="*60)
        print("🔍 ANALISADOR DE FREQUÊNCIA DE PALAVRAS")
        print("="*60)
        
        while True:
            print("\nEscolha o tipo de análise:")
            print("1. 📄 Analisar um arquivo único")
            print("2. 📁 Analisar pasta com múltiplos arquivos") 
            print("3. ❌ Sair")
            
            choice = input("\nDigite sua escolha (1-3): ").strip()
            
            if choice == '1':
                self._analyze_single_file()
            elif choice == '2':
                self._analyze_multiple_files()
            elif choice == '3':
                print("👋 Encerrando programa...")
                break
            else:
                print("❌ Opção inválida! Tente novamente.")
    
    def _analyze_single_file(self):
        """Análise de arquivo único"""
        print("\n📄 ANÁLISE DE ARQUIVO ÚNICO")
        print("-" * 40)
        
        file_path = input("Digite o caminho completo do arquivo: ").strip()
        if not file_path:
            file_path = os.path.expanduser("~/Downloads/corpus.txt")
            print(f"Usando caminho padrão: {file_path}")
        
        self.texts = []  # Reset
        self.load_text_file(file_path)
        
        if not self.texts:
            print("❌ Nenhum arquivo foi carregado!")
            return
        
        self._run_analysis()
    
    def _analyze_multiple_files(self):
        """Análise de múltiplos arquivos"""
        print("\n📁 ANÁLISE DE MÚLTIPLOS ARQUIVOS")
        print("-" * 40)
        
        folder_path = input("Digite o caminho da pasta: ").strip()
        if not folder_path:
            folder_path = r"C:\Users\PICHAU\Downloads\artigos_selecionados\artigos\ciencia_de_dados"
            print(f"Usando caminho padrão: {folder_path}")
        
        print("\nEscolha o método de carregamento:")
        print("1. Todos os arquivos da pasta")
        print("2. Apenas arquivos específicos (.txt, .md, .docx)")
        
        load_choice = input("Digite sua escolha (1-2): ").strip()
        
        self.texts = []  # Reset
        
        if load_choice == '2':
            files_loaded = self.load_folder(folder_path)
        else:
            files_loaded = self.load_all_files_from_folder(folder_path)
        
        if files_loaded == 0:
            print("❌ Nenhum arquivo foi carregado!")
            return
        
        self._run_analysis()
    
    def _run_analysis(self):
        """Executa a análise com as palavras especificadas"""
        print(f"\n✅ {len(self.texts)} arquivo(s) carregado(s)")
        
        # Definir palavras-alvo
        print("\nDefina as palavras para análise:")
        words_input = input("Digite as palavras separadas por vírgula: ").strip()
        
        if not words_input:
            palavras_alvo = ["architecture", "security", "privacy"]  # Padrão do seu exemplo
            print(f"Usando palavras padrão: {palavras_alvo}")
        else:
            palavras_alvo = [word.strip() for word in words_input.split(',')]
        
        print(f"🔍 Analisando palavras: {palavras_alvo}")
        
        # Realizar análise
        self.analyze_frequency(palavras_alvo)
        
        # Mostrar resultados básicos
        print("\n" + "="*50)
        print("📊 RESULTADOS DA ANÁLISE")
        print("="*50)
        
        df_results = self.create_frequency_dataframe()
        print("\n📋 Resumo dos dados:")
        print(df_results)
        
        print("\n📈 Estatísticas:")
        print(self.get_summary_stats())
        
        # Menu de visualizações
        self._visualization_menu(palavras_alvo)
    
    def _visualization_menu(self, palavras_alvo):
        """Menu para escolher visualizações"""
        while True:
            print("\n" + "="*50)
            print("📊 OPÇÕES DE VISUALIZAÇÃO")
            print("="*50)
            print("1. 📊 Gráfico de barras horizontais")
            print("2. 📈 Gráfico de barras verticais")
            print("3. 🔥 Mapa de calor (múltiplos arquivos)")
            print("4. 🔄 Comparação individual (múltiplos arquivos)")
            print("5. 📋 Relatório detalhado (múltiplos arquivos)")
            print("6. 💾 Exportar para CSV")
            print("7. ↩️  Voltar ao menu principal")
            
            viz_choice = input("\nEscolha a visualização (1-7): ").strip()
            
            if viz_choice == '1':
                self.plot_frequency_bar(horizontal=True, title="Frequência das Palavras-Chave (Horizontal)")
            elif viz_choice == '2':
                self.plot_frequency_bar(horizontal=False, title="Frequência das Palavras-Chave (Vertical)")
            elif viz_choice == '3':
                self.plot_frequency_heatmap()
            elif viz_choice == '4':
                self.plot_individual_comparison(palavras_alvo)
            elif viz_choice == '5':
                if len(self.texts) > 1:
                    self.create_detailed_report(palavras_alvo)
                else:
                    print("📋 Relatório detalhado disponível apenas para múltiplos arquivos.")
            elif viz_choice == '6':
                filename = input("Nome do arquivo CSV (ou Enter para padrão): ").strip()
                if not filename:
                    filename = "resultados_mineracao.csv"
                if not filename.endswith('.csv'):
                    filename += '.csv'
                self.export_results_to_csv(palavras_alvo, filename)
            elif viz_choice == '7':
                break
            else:
                print("❌ Opção inválida!")

# Exemplo de uso direto (sem menu interativo)
def exemplo_uso_direto():
    """Função de exemplo para uso direto do código"""
    analyzer = TextFrequencyAnalyzer()
    
    # Exemplo 1: Arquivo único
    caminho_corpus = os.path.expanduser("~/Downloads/corpus.txt")
    analyzer.load_text_file(caminho_corpus)
    
    # Exemplo 2: Múltiplos arquivos (descomente para usar)
    # pasta_artigos = r"C:\Users\PICHAU\Downloads\artigos_selecionados\artigos\ciencia_de_dados"
    # analyzer.load_all_files_from_folder(pasta_artigos)
    
    # Palavras para analisar
    palavras_alvo = ["architecture", "security", "privacy"]
    
    if analyzer.texts:
        # Análise
        analyzer.analyze_frequency(palavras_alvo)
        
        # Resultados
        print("=== ANÁLISE DE FREQUÊNCIA DE PALAVRAS ===")
        print(analyzer.create_frequency_dataframe())
        print("\nEstatísticas:")
        print(analyzer.get_summary_stats())
        
        # Visualizações
        analyzer.plot_frequency_bar(horizontal=True)
        analyzer.plot_frequency_heatmap()
        
        # Exportar
        analyzer.export_results_to_csv(palavras_alvo)

# Ponto de entrada principal
if __name__ == "__main__":
    # Opção 1: Menu interativo (recomendado)
    analyzer = TextFrequencyAnalyzer()
    analyzer.interactive_menu()
    
    # Opção 2: Uso direto (descomente para usar)
    # exemplo_uso_direto()