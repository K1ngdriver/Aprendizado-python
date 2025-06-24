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
            with open(file_path, 'r', encoding=encoding) as file:
                text = file.read()
                file_name = Path(file_path).stem
                self.add_text(text, file_name)
                print(f"Arquivo '{file_name}' carregado com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")
    
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
    
    def plot_individual_comparison(self, target_words, case_sensitive=False, figsize=(15, 8)):
        """Cria gráfico comparando palavras entre diferentes arquivos"""
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
        
        plt.title('Frequência de Palavras por Arquivo', fontsize=16, fontweight='bold')
        plt.xlabel('Arquivos', fontsize=12)
        plt.ylabel('Frequência', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Palavras', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
        
        # Gráfico de heatmap
        if len(individual_results) > 1:
            plt.figure(figsize=(12, 8))
            sns.heatmap(pivot_df.T, annot=True, cmap='YlOrRd', fmt='g', cbar_kws={'label': 'Frequência'})
            plt.title('Mapa de Calor - Distribuição de Palavras por Arquivo', fontsize=14, fontweight='bold')
            plt.xlabel('Arquivos', fontsize=12)
            plt.ylabel('Palavras', fontsize=12)
            plt.tight_layout()
            plt.show()
    
    def export_results_to_csv(self, target_words, filename="resultados_mineracao.csv", case_sensitive=False):
        """Exporta resultados para CSV"""
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
        df_csv.to_csv(filename, index=False, encoding='utf-8')
        print(f"✓ Resultados exportados para: {filename}")
        return df_csv
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
            print(f"Erro: Pasta não encontrada: {folder_path}")
            return
        
        files_loaded = 0
        
        # Procurar por todos os tipos de arquivo
        for ext in file_extensions:
            pattern = folder_path / f"*{ext}"
            files = glob.glob(str(pattern))
            
            for file_path in files:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
                        text = file.read()
                        file_name = Path(file_path).stem
                        self.add_text(text, file_name)
                        files_loaded += 1
                        print(f"✓ Arquivo carregado: {file_name}")
                except Exception as e:
                    print(f"✗ Erro ao carregar {file_path}: {e}")
        
        if files_loaded == 0:
            print(f"Nenhum arquivo encontrado em: {folder_path}")
            print(f"Extensões procuradas: {file_extensions}")
        else:
            print(f"\nTotal de arquivos carregados: {files_loaded}")
    
    def load_all_files_from_folder(self, folder_path, encoding='utf-8'):
        """
        Carrega TODOS os arquivos de uma pasta, independente da extensão
        """
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            print(f"Erro: Pasta não encontrada: {folder_path}")
            return
        
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
            print(f"Nenhum arquivo de texto encontrado em: {folder_path}")
        else:
            print(f"\nTotal de arquivos carregados: {files_loaded}")
    
    
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
        """Cria gráfico de barras da frequência das palavras"""
        df = self.create_frequency_dataframe()
        
        plt.figure(figsize=figsize)
        
        if len(self.texts) == 1:
            # Se há apenas um texto, mostra frequência simples
            word_totals = df.groupby('palavra')['frequencia'].sum().sort_values(ascending=False)
            plt.bar(word_totals.index, word_totals.values)
            plt.title(title)
            plt.xlabel('Palavras')
            plt.ylabel('Frequência')
            plt.xticks(rotation=45)
        else:
            # Se há múltiplos textos, mostra comparação
            pivot_df = df.pivot(index='palavra', columns='fonte', values='frequencia').fillna(0)
            pivot_df.plot(kind='bar', figsize=figsize)
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
    
    # CONFIGURAÇÃO PARA SUA PASTA DE ARTIGOS
    pasta_artigos = r"C:\Users\PICHAU\Downloads\artigos_selecionados\artigos\ciencia_de_dados"
    
    print("=== CARREGANDO ARQUIVOS DA PASTA ===")
    
    # OPÇÃO 1: Carregar apenas arquivos específicos (.txt, .md, etc.)
    # analyzer.load_folder(pasta_artigos, file_extensions=['.txt', '.md', '.doc'])
    
    # OPÇÃO 2: Carregar TODOS os arquivos da pasta (recomendado)
    analyzer.load_all_files_from_folder(pasta_artigos)
    
    # Verificar se arquivos foram carregados
    if not analyzer.texts:
        print("❌ Nenhum arquivo foi carregado!")
        print("Verifique se:")
        print("1. O caminho está correto")
        print("2. Existem arquivos na pasta")
        print("3. Os arquivos contêm texto")
        
        # Tentar caminhos alternativos
        caminhos_alternativos = [
            r"C:\Users\PICHAU\Downloads\artigos_selecionados\artigos",
            r"C:\Users\PICHAU\Downloads\artigos_selecionados",
            r"C:\Users\PICHAU\Downloads"
        ]
        
        print("\nTentando caminhos alternativos...")
        for caminho in caminhos_alternativos:
            if os.path.exists(caminho):
                print(f"✓ Pasta encontrada: {caminho}")
                arquivos = list(Path(caminho).iterdir())
                print(f"  Arquivos na pasta: {len([f for f in arquivos if f.is_file()])}")
                break
            else:
                print(f"✗ Pasta não encontrada: {caminho}")
    
    else:
        print(f"✅ {len(analyzer.texts)} arquivos carregados com sucesso!")
        
        # SUAS PALAVRAS-CHAVE PARA ANÁLISE
        # *** MODIFIQUE AQUI COM AS PALAVRAS QUE VOCÊ QUER ANALISAR ***
        palavras_alvo = [
            "architecture", "security","privacy"
        ]
        
        print(f"\n=== ANALISANDO PALAVRAS: {palavras_alvo} ===")
        
        # ANÁLISE COMPLETA
        print("\n1. RELATÓRIO DETALHADO POR ARQUIVO:")
        resultados_individuais = analyzer.create_detailed_report(palavras_alvo)
        
        print("\n2. ANÁLISE GERAL:")
        analyzer.analyze_frequency(palavras_alvo)
        df_results = analyzer.create_frequency_dataframe()
        print(df_results.head(10))
        
        print("\n3. ESTATÍSTICAS RESUMIDAS:")
        print(analyzer.get_summary_stats())
        
        # VISUALIZAÇÕES
        print("\n4. GERANDO GRÁFICOS...")
        
        # Gráfico comparativo entre arquivos
        analyzer.plot_individual_comparison(palavras_alvo)
        
        # Gráfico geral
        analyzer.plot_frequency_bar(title="Frequência Total das Palavras-Chave")
        
        # EXPORTAR RESULTADOS
        print("\n5. EXPORTANDO RESULTADOS...")
        df_exportado = analyzer.export_results_to_csv(
            palavras_alvo, 
            filename="analise_artigos_ciencia_dados.csv"
        )
        
        print("\n=== RESUMO FINAL ===")
        print(f"📁 Arquivos analisados: {len(analyzer.texts)}")
        print(f"🔍 Palavras pesquisadas: {len(palavras_alvo)}")
        print(f"📊 Resultados exportados para: analise_artigos_ciencia_dados.csv")
        
        # Mostrar os 5 arquivos com mais ocorrências
        print("\n🏆 TOP 5 ARQUIVOS COM MAIS PALAVRAS-CHAVE:")
        totais_por_arquivo = {}
        for arquivo, dados in resultados_individuais.items():
            total = sum(dados['palavras_encontradas'].values())
            totais_por_arquivo[arquivo] = total
        
        top_5 = sorted(totais_por_arquivo.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (arquivo, total) in enumerate(top_5, 1):
            print(f"{i}. {arquivo}: {total} ocorrências")
    
    print("\n=== INSTRUÇÕES PARA PERSONALIZAR ===")
    print("1. Modifique a variável 'palavras_alvo' com suas palavras")
    print("2. Ajuste o caminho 'pasta_artigos' se necessário")
    print("3. Execute o código")
    print("4. Os resultados serão salvos em CSV automaticamente")
    
    # Função para listar arquivos da pasta (diagnóstico)
    def diagnosticar_pasta(caminho):
        """Função para diagnosticar problemas na pasta"""
        print(f"\n=== DIAGNÓSTICO DA PASTA ===")
        print(f"Caminho: {caminho}")
        
        if not os.path.exists(caminho):
            print("❌ Pasta não existe!")
            return
        
        pasta = Path(caminho)
        arquivos = list(pasta.iterdir())
        
        print(f"Total de itens: {len(arquivos)}")
        print(f"Arquivos: {len([f for f in arquivos if f.is_file()])}")
        print(f"Pastas: {len([f for f in arquivos if f.is_dir()])}")
        
        print("\nPrimeiros 10 arquivos encontrados:")
        arquivos_apenas = [f for f in arquivos if f.is_file()][:10]
        for arquivo in arquivos_apenas:
            print(f"  - {arquivo.name} ({arquivo.suffix})")
    
    # Descomente para diagnosticar sua pasta:
    # diagnosticar_pasta(pasta_artigos)