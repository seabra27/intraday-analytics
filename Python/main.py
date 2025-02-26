import os
import time
import logging
import pandas as pd
import requests
import zipfile
import shutil
import glob
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv, find_dotenv

# Configuração do logging
logging.basicConfig(filename='log_extracao.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Forçar recarregamento das variáveis de ambiente
load_dotenv(find_dotenv(), override=True)

# Configurações gerais
PASTA_DESTINO = "data/raw"
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}
URLS_APIS = {
    "FORECAST": "https://api.airtable.com/v0/appMDw883DjY0pMej/Result%201",
    "DEPARA_SKILL": "https://api.airtable.com/v0/appnlzAmDtFtGBjyt/Result%201"
}

# Criando pasta de destino se não existir
os.makedirs(PASTA_DESTINO, exist_ok=True)

# Variáveis globais para os DataFrames
df_concatenado_hsplit = None
df_concatenado_hagent = None

def baixar_arquivo_kangle():
    """Automatiza login e download dos arquivos XLSX via Selenium"""
    logging.info("Iniciando automação com Selenium...")
    
    # Obtém as credenciais do arquivo .env
    email = os.getenv('KAGGLE_EMAIL')
    senha = os.getenv('KAGGLE_PASSWORD')
        
    if not email or not senha:
        logging.error("Credenciais do Kaggle não encontradas no arquivo .env")
        raise ValueError("Configure as variáveis KAGGLE_EMAIL e KAGGLE_PASSWORD no arquivo .env")
    
    options = webdriver.ChromeOptions()
    # Configurar o diretório de download
    prefs = {
        "download.default_directory": os.path.abspath(PASTA_DESTINO),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Criando diretório de destino se não existir
        os.makedirs(PASTA_DESTINO, exist_ok=True)
        
        # Acessando página de login do Kaggle
        driver.get("https://www.kaggle.com/account/login?phase=emailSignIn&returnUrl=%2F")
        time.sleep(3)  # Aguarda carregamento da página

        # Realizando login
        email_field = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[1]/form/div/div[1]/div/input')
        password_field = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[1]/form/div/div[2]/div/input')

        email_field.send_keys(email)
        password_field.send_keys(senha)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)  # Aguarda processamento do login

        # Após login, acessa a página do dataset
        driver.get("https://www.kaggle.com/datasets/thomassimeo/volumetria-tempos-fictcios")
        time.sleep(5)  # Aumentado o tempo de espera para garantir carregamento

        # Localizar e clicar no botão de download do arquivo zip
        download_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/button')
        download_button.click()
        time.sleep(3)  # Aguarda o menu aparecer

        # Clica no segundo botão para iniciar o download
        second_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/ul/li[1]')
        second_button.click()
        time.sleep(10)  # Aguarda o download completar

        logging.info("Download do arquivo zip realizado com sucesso!")
    
    except Exception as e:
        logging.error(f"Erro ao baixar arquivos: {e}")

    finally:
        driver.quit()

def baixar_arquivo_api(nome, url):
    """Faz requisição GET para a API e salva os dados"""
    logging.info(f"Baixando {nome}.csv da API...")
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            # Processa os dados extraindo campos corretamente
            if "records" in data:
                registros = []
                for record in data["records"]:
                    registro = {"id": record["id"]}
                    registro.update(record.get("fields", {}))
                    registros.append(registro)
                
                df = pd.DataFrame(registros)
                # Alterado para salvar direto na pasta process
                pasta_process = "data/process"
                os.makedirs(pasta_process, exist_ok=True)
                caminho_arquivo = os.path.join(pasta_process, f"{nome}.csv")
                df.to_csv(caminho_arquivo, index=False)
                logging.info(f"{nome}.csv salvo com sucesso em {caminho_arquivo}!")
            else:
                logging.error(f"Formato de dados inesperado para {nome}")
        else:
            logging.error(f"Erro ao baixar {nome}: {response.status_code}")
    except Exception as e:
        logging.error(f"Erro ao processar API {nome}: {e}")

def converter_xlsx_para_csv():
    """Converte arquivos XLSX baixados para CSV"""
    logging.info("Convertendo arquivos XLSX para CSV...")
    for arquivo in os.listdir(PASTA_DESTINO):
        if arquivo.endswith(".xlsx"):
            caminho = os.path.join(PASTA_DESTINO, arquivo)
            df = pd.read_excel(caminho)
            df.to_csv(caminho.replace(".xlsx", ".csv"), index=False)
            os.remove(caminho)
            logging.info(f"{arquivo} convertido para CSV e removido.")

def verificar_data_mais_recente(pasta_process, prefixo):
    """Verifica a data mais recente dos arquivos com determinado prefixo na pasta process"""
    arquivos = glob.glob(os.path.join(pasta_process, f"{prefixo}*.csv"))
    if not arquivos:
        return None
    
    try:
        # Extrai a data do nome do arquivo
        def extrair_data_arquivo(arquivo):
            try:
                data_str = arquivo.split('_')[-1].replace('.csv', '')
                return datetime.strptime(data_str, '%Y-%m-%d')
            except:
                return datetime.min
        
        # Encontra a data mais recente
        data_mais_recente = max(arquivos, key=extrair_data_arquivo)
        return extrair_data_arquivo(data_mais_recente)
    except Exception as e:
        logging.error(f"Erro ao verificar data mais recente para {prefixo}: {e}")
        return None

def processar_arquivos_raw():
    """Processa arquivos da pasta raw, verificando duplicidade com a pasta process"""
    logging.info("Verificando arquivos na pasta raw...")
    
    pasta_process = "data/process"
    os.makedirs(pasta_process, exist_ok=True)
    
    # Verifica as datas mais recentes dos arquivos existentes
    data_hsplit = verificar_data_mais_recente(pasta_process, "HSPLIT")
    data_hagent = verificar_data_mais_recente(pasta_process, "HAGENT")
    
    # Lista todos os arquivos xlsx na pasta raw
    for arquivo in os.listdir(PASTA_DESTINO):
        if arquivo.endswith('.xlsx'):
            nome_base = os.path.splitext(arquivo)[0]
            
            # Extrai a data do arquivo atual
            try:
                data_arquivo = datetime.strptime(nome_base.split('_')[-1], '%Y-%m-%d')
            except:
                # Se não conseguir extrair a data, processa o arquivo normalmente
                data_arquivo = None
            
            # Verifica se é necessário processar o arquivo
            if nome_base.startswith('HSPLIT') and data_hsplit and data_arquivo:
                if data_arquivo <= data_hsplit:
                    logging.info(f"Arquivo {arquivo} ignorado pois já existe versão mais recente em process")
                    os.remove(os.path.join(PASTA_DESTINO, arquivo))
                    continue
                    
            elif nome_base.startswith('HAGENT') and data_hagent and data_arquivo:
                if data_arquivo <= data_hagent:
                    logging.info(f"Arquivo {arquivo} ignorado pois já existe versão mais recente em process")
                    os.remove(os.path.join(PASTA_DESTINO, arquivo))
                    continue
            
            # Se chegou aqui, processa o arquivo normalmente
            arquivo_process = os.path.join(pasta_process, nome_base + '.csv')
            origem = os.path.join(PASTA_DESTINO, arquivo)
            
            # Converte xlsx para csv diretamente na pasta process
            df = pd.read_excel(origem)
            df.to_csv(arquivo_process, index=False)
            
            # Remove o arquivo xlsx original
            os.remove(origem)
            logging.info(f"Arquivo {arquivo} convertido para CSV e movido para {pasta_process}")

def processar_forecast():
    """Processa o arquivo FORECAST.csv normalizando a coluna fields que contém JSON"""
    logging.info("Processando arquivo FORECAST.csv...")
    
    arquivo_forecast = os.path.join(PASTA_DESTINO, "FORECAST.csv")
    if not os.path.exists(arquivo_forecast):
        logging.error("Arquivo FORECAST.csv não encontrado")
        return
    
    try:
        # Lê o arquivo CSV
        df = pd.read_csv(arquivo_forecast)
        
        def parse_json_seguro(x):
            try:
                # Remove caracteres especiais e escapes problemáticos
                x = x.replace('\\', '')
                x = x.replace('\xa0', ' ')
                x = x.replace("'", '"')
                
                # Trata casos especiais de aspas
                import re
                x = re.sub(r'"([^"]+)"s"', r'"\1s"', x)
                
                try:
                    return json.loads(x)
                except:
                    valores = re.findall(r'"([^"]*)"', x)
                    for valor in valores:
                        if '"' in valor:
                            novo_valor = valor.replace('"', '')
                            x = x.replace(f'"{valor}"', f'"{novo_valor}"')
                    return json.loads(x)
                
            except Exception as e:
                logging.error(f"Erro ao processar JSON: {e} - Valor: {x}")
                return {}
        
        # Converte a string JSON em dicionário
        df['fields'] = df['fields'].apply(parse_json_seguro)
        
        # Normaliza o JSON da coluna fields
        df_normalizado = pd.json_normalize(df['fields'])
        
        # Combina as colunas
        df_final = pd.concat([df[['id', 'createdTime']], df_normalizado], axis=1)
        
        # Remove caracteres especiais
        df_final.columns = df_final.columns.str.replace('\xa0', '')
        
        # Salva o arquivo processado
        pasta_process = "data/process"
        os.makedirs(pasta_process, exist_ok=True)
        caminho_saida = os.path.join(pasta_process, "FORECAST.csv")
        df_final.to_csv(caminho_saida, index=False, encoding='utf-8')
        
        logging.info(f"Arquivo FORECAST processado e salvo em {caminho_saida}")
        os.remove(arquivo_forecast)
        
    except Exception as e:
        logging.error(f"Erro ao processar FORECAST.csv: {e}")

def processar_depara_skill():
    """Processa o arquivo DEPARA_SKILL.csv normalizando a coluna fields que contém JSON"""
    logging.info("Processando arquivo DEPARA_SKILL.csv...")
    
    arquivo_depara = os.path.join(PASTA_DESTINO, "DEPARA_SKILL.csv")
    if not os.path.exists(arquivo_depara):
        logging.error("Arquivo DEPARA_SKILL.csv não encontrado")
        return
    
    try:
        # Lê o arquivo CSV
        df = pd.read_csv(arquivo_depara)
        
        def parse_json_seguro(x):
            try:
                # Remove caracteres especiais e escapes problemáticos
                x = x.replace('\\', '')
                x = x.replace('\xa0', ' ')
                
                # Substitui aspas simples por duplas para formato JSON válido
                x = x.replace("'", '"')
                
                # Trata o caso específico de "IP RH"s" e similares
                import re
                # Encontra padrões como "texto"s" e substitui por "textos"
                x = re.sub(r'"([^"]+)"s"', r'"\1s"', x)
                
                # Se ainda houver erro, tenta uma abordagem mais agressiva
                try:
                    return json.loads(x)
                except:
                    # Remove todas as aspas duplas que estão dentro de valores já entre aspas
                    valores = re.findall(r'"([^"]*)"', x)
                    for valor in valores:
                        if '"' in valor:
                            novo_valor = valor.replace('"', '')
                            x = x.replace(f'"{valor}"', f'"{novo_valor}"')
                    return json.loads(x)
                
            except Exception as e:
                logging.error(f"Erro ao processar JSON: {e} - Valor: {x}")
                return {}
        
        # Converte a string JSON em dicionário com tratamento de erros
        df['fields'] = df['fields'].apply(parse_json_seguro)
        
        # Normaliza o JSON da coluna fields (expande o dicionário em colunas)
        df_normalizado = pd.json_normalize(df['fields'])
        
        # Combina as colunas originais com as novas colunas normalizadas
        df_final = pd.concat([df[['id', 'createdTime']], df_normalizado], axis=1)
        
        # Remove caracteres especiais dos nomes das colunas
        df_final.columns = df_final.columns.str.replace('\xa0', '')
        
        # Salva o arquivo processado
        pasta_process = "data/process"
        os.makedirs(pasta_process, exist_ok=True)
        caminho_saida = os.path.join(pasta_process, "DEPARA_SKILL.csv")
        df_final.to_csv(caminho_saida, index=False, encoding='utf-8')
        
        logging.info(f"Arquivo DEPARA_SKILL processado e salvo em {caminho_saida}")
        
        # Log das colunas encontradas e uma amostra dos dados
        logging.info(f"Colunas no arquivo processado: {', '.join(df_final.columns)}")
        logging.info(f"Primeiras linhas do arquivo processado:\n{df_final.head().to_string()}")
        
        # Remove o arquivo original da pasta raw
        os.remove(arquivo_depara)
        logging.info("Arquivo DEPARA_SKILL.csv processado com sucesso e removido da pasta raw!")
        
    except Exception as e:
        logging.error(f"Erro ao processar DEPARA_SKILL.csv: {e}")

def extrair_e_mover_arquivos():
    """Extrai arquivos do ZIP e move para a pasta process"""
    logging.info("Iniciando extração de arquivos ZIP...")
    
    try:
        # Procura pelo arquivo zip na pasta raw
        for arquivo in os.listdir(PASTA_DESTINO):
            if arquivo.endswith(".zip"):
                caminho_zip = os.path.join(PASTA_DESTINO, arquivo)
                
                # Lista os arquivos existentes na pasta raw
                arquivos_existentes = {os.path.splitext(f)[0] for f in os.listdir(PASTA_DESTINO)}
                
                # Lista os arquivos dentro do ZIP
                with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                    arquivos_zip = {os.path.splitext(f)[0] for f in zip_ref.namelist()}
                
                # Verifica se há conflito de nomes
                conflitos = arquivos_zip.intersection(arquivos_existentes)
                
                if conflitos:
                    logging.warning(f"Arquivos com nomes conflitantes encontrados: {conflitos}")
                    logging.warning("Extração do ZIP cancelada para evitar sobrescrita")
                    continue
                
                # Se não houver conflitos, extrai os arquivos
                with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                    zip_ref.extractall(PASTA_DESTINO)
                    logging.info(f"Arquivo {arquivo} extraído com sucesso")
                
                # Remove o arquivo zip
                os.remove(caminho_zip)
                logging.info(f"Arquivo ZIP removido")
                
    except Exception as e:
        logging.error(f"Erro ao extrair arquivos: {e}")

def concatenar_arquivos():
    """Concatena arquivos que começam com HSPLIT e HAGENT na pasta process"""
    logging.info("Iniciando concatenação dos arquivos HSPLIT e HAGENT...")
    
    pasta_process = "data/process"
    try:
        # Função auxiliar para extrair data do nome do arquivo
        def extrair_data_arquivo(arquivo):
            try:
                # Extrai a data do nome do arquivo (formato: TIPO_YYYY-MM-DD.csv)
                data_str = arquivo.split('_')[-1].replace('.csv', '')
                return datetime.strptime(data_str, '%Y-%m-%d')
            except:
                return datetime.min
        
        # Concatenar arquivos HSPLIT
        arquivos_hsplit = glob.glob(os.path.join(pasta_process, "HSPLIT*.csv"))
        if arquivos_hsplit:
            # Encontra a data mais recente
            data_mais_recente = max(arquivos_hsplit, key=extrair_data_arquivo)
            data_nome = extrair_data_arquivo(data_mais_recente).strftime('%Y-%m-%d')
            
            # Concatena os arquivos mantendo a coluna row_date
            dfs_hsplit = []
            for arquivo in arquivos_hsplit:
                df = pd.read_csv(arquivo, low_memory=False)
                if 'row_date' in df.columns:
                    dfs_hsplit.append(df)
                else:
                    logging.warning(f"Arquivo {arquivo} não contém a coluna row_date")
            
            if dfs_hsplit:
                df_concatenado_hsplit = pd.concat(dfs_hsplit, ignore_index=True)
                
                # Salva com o nome contendo a data mais recente
                nome_arquivo = f"HSPLIT_{data_nome}.csv"
                caminho_arquivo_final = os.path.join(pasta_process, nome_arquivo)
                df_concatenado_hsplit.to_csv(caminho_arquivo_final, index=False)
                
                # Remove os arquivos originais
                for arquivo in arquivos_hsplit:
                    if arquivo != caminho_arquivo_final:
                        os.remove(arquivo)
                        logging.info(f"Arquivo original removido: {os.path.basename(arquivo)}")
                
                logging.info(f"Arquivos HSPLIT concatenados com sucesso em {nome_arquivo}!")
        
        # Concatenar arquivos HAGENT (mesmo processo)
        arquivos_hagent = glob.glob(os.path.join(pasta_process, "HAGENT*.csv"))
        if arquivos_hagent:
            data_mais_recente = max(arquivos_hagent, key=extrair_data_arquivo)
            data_nome = extrair_data_arquivo(data_mais_recente).strftime('%Y-%m-%d')
            
            dfs_hagent = []
            for arquivo in arquivos_hagent:
                df = pd.read_csv(arquivo, low_memory=False)
                if 'row_date' in df.columns:
                    dfs_hagent.append(df)
                else:
                    logging.warning(f"Arquivo {arquivo} não contém a coluna row_date")
            
            if dfs_hagent:
                df_concatenado_hagent = pd.concat(dfs_hagent, ignore_index=True)
                
                nome_arquivo = f"HAGENT_{data_nome}.csv"
                caminho_arquivo_final = os.path.join(pasta_process, nome_arquivo)
                df_concatenado_hagent.to_csv(caminho_arquivo_final, index=False)
                
                for arquivo in arquivos_hagent:
                    if arquivo != caminho_arquivo_final:
                        os.remove(arquivo)
                        logging.info(f"Arquivo original removido: {os.path.basename(arquivo)}")
                
                logging.info(f"Arquivos HAGENT concatenados com sucesso em {nome_arquivo}!")
            
    except Exception as e:
        logging.error(f"Erro ao concatenar arquivos: {e}")

def remover_duplicatas_process():
    """Remove linhas duplicadas de todos os arquivos CSV na pasta process"""
    logging.info("Iniciando remoção de duplicatas dos arquivos CSV na pasta process...")
    
    pasta_process = "data/process"
    try:
        # Lista todos os arquivos CSV na pasta process
        arquivos_csv = glob.glob(os.path.join(pasta_process, "*.csv"))
        
        for arquivo in arquivos_csv:
            try:
                # Lê o arquivo CSV com low_memory=False para evitar DtypeWarning
                df = pd.read_csv(arquivo, low_memory=False)
                
                # Registra o número de linhas antes da remoção
                linhas_antes = len(df)
                
                # Remove duplicatas
                df = df.drop_duplicates()
                
                # Registra o número de linhas após a remoção
                linhas_depois = len(df)
                
                # Salva o arquivo sem as duplicatas
                df.to_csv(arquivo, index=False)
                
                duplicatas_removidas = linhas_antes - linhas_depois
                if duplicatas_removidas > 0:
                    logging.info(f"Arquivo {os.path.basename(arquivo)}: {duplicatas_removidas} linhas duplicadas removidas")
                else:
                    logging.info(f"Arquivo {os.path.basename(arquivo)}: nenhuma duplicata encontrada")
                    
            except Exception as e:
                logging.error(f"Erro ao processar arquivo {os.path.basename(arquivo)}: {e}")
                
    except Exception as e:
        logging.error(f"Erro ao remover duplicatas: {e}")

def analisar_e_otimizar_colunas(df, tipo_arquivo):
    """Analisa e otimiza as colunas do DataFrame para reduzir uso de memória"""
    logging.info(f"Otimizando colunas do arquivo {tipo_arquivo}...")
    
    for coluna in df.columns:
        # Identifica colunas que são completamente nulas
        if df[coluna].isna().all():
            df[coluna] = df[coluna].astype('category')
            continue
            
        # Tenta converter para o tipo mais eficiente
        try:
            # Verifica se a coluna contém apenas zeros e números inteiros
            if df[coluna].dtype in ['float64', 'int64']:
                # Se todos os valores são zero ou inteiros, converte para inteiro
                if (df[coluna] == 0).all() or df[coluna].dropna().apply(lambda x: float(x).is_integer()).all():
                    df[coluna] = pd.to_numeric(df[coluna], downcast='integer')
                else:
                    df[coluna] = pd.to_numeric(df[coluna], downcast='float')
            # Para colunas de texto
            elif df[coluna].dtype == 'object':
                # Se a coluna tem poucos valores únicos, converte para categoria
                if df[coluna].nunique() / len(df[coluna]) < 0.5:
                    df[coluna] = df[coluna].astype('category')
        except:
            # Se falhar a conversão, mantém o tipo original
            pass
    
    return df

def tratar_hagent(arquivo_entrada, pasta_saida="data/process"):
    """Processa o arquivo HAGENT.csv para otimizar os KPIs necessários."""
    try:
        os.makedirs(pasta_saida, exist_ok=True)
        df = pd.read_csv(arquivo_entrada, low_memory=False)
        
        # Seleção e renomeação das colunas
        df = df[["row_date", "i_stafftime", "ti_auxtime", "ti_auxtime1", "ti_auxtime3", "i_availtime"]].copy()
        df.rename(columns={
            "row_date": "Data",
            "i_stafftime": "TempoLogado",
            "ti_auxtime": "TempoPausa",
            "ti_auxtime1": "Pausa1Lanche",
            "ti_auxtime3": "Pausa3Descanso",
            "i_availtime": "Disponível"
        }, inplace=True)
        
        # Converte Data para datetime e as outras colunas para float32
        df["Data"] = pd.to_datetime(df["Data"])
        colunas_numericas = df.columns.difference(["Data"])
        df[colunas_numericas] = df[colunas_numericas].astype("float32")
        
        # Cálculo das métricas com tratamento para divisão por zero
        df["% Pausas"] = df.apply(lambda x: (x["TempoPausa"] / x["TempoLogado"]) * 100 if x["TempoLogado"] > 0 else 0, axis=1)
        df["% Pausas NR17"] = df.apply(lambda x: ((x["Pausa1Lanche"] + x["Pausa3Descanso"]) / x["TempoLogado"]) * 100 if x["TempoLogado"] > 0 else 0, axis=1)
        df["% Outras Pausas"] = df.apply(lambda x: ((x["TempoPausa"] - x["Pausa1Lanche"] - x["Pausa3Descanso"]) / x["TempoLogado"]) * 100 if x["TempoLogado"] > 0 else 0, axis=1)
        df["% Ocupação"] = df.apply(lambda x: ((x["TempoLogado"] - x["TempoPausa"] - x["Disponível"]) / (x["TempoLogado"] - x["TempoPausa"])) * 100 if (x["TempoLogado"] - x["TempoPausa"]) > 0 else 0, axis=1)
        
        df.drop(columns=["TempoPausa", "Pausa1Lanche", "Pausa3Descanso", "Disponível"], inplace=True)
        
        arquivo_saida = os.path.join(pasta_saida, "HAGENT.csv")
        df.to_csv(arquivo_saida, index=False, encoding="utf-8")
        logging.info(f"Arquivo processado e salvo em: {arquivo_saida}")
        return True
    except Exception as e:
        logging.error(f"Erro ao processar HAGENT.csv: {e}")
        return False

def processar_chunk_hsplit(chunk):
    """Processa um chunk do arquivo HSPLIT."""
    try:
        # Define as colunas necessárias
        colunas_hsplit = {
            "row_date": "Data",
            "callsoffered": "ChamadasRecebidas",
            "acdcalls": "ChamadasAtendidas",
            "acdcalls1": "ChamadasAtendidasNs",
            "abncalls1": "AbandonadasNs",
            "acdtime": "TempoFaladoTotal",
            "ringtime": "TempoEspera",
            "transferred": "ChamadasTransferidas"
        }
        
        # Seleciona e renomeia colunas
        chunk = chunk[list(colunas_hsplit.keys())].copy()
        chunk.rename(columns=colunas_hsplit, inplace=True)
        
        # Converte tipos
        chunk["Data"] = pd.to_datetime(chunk["Data"])
        colunas_numericas = chunk.columns.difference(["Data"])
        chunk[colunas_numericas] = chunk[colunas_numericas].astype("float32")
        
        # Calcula métricas
        chunk["NS"] = chunk.apply(lambda x: (x["ChamadasAtendidasNs"] / (x["ChamadasRecebidas"] - x["AbandonadasNs"])) * 100 
                                if (x["ChamadasRecebidas"] - x["AbandonadasNs"]) > 0 else 0, axis=1)
        chunk["TMA"] = chunk.apply(lambda x: x["TempoFaladoTotal"] / x["ChamadasAtendidas"] 
                                if x["ChamadasAtendidas"] > 0 else 0, axis=1)
        chunk["TME"] = chunk.apply(lambda x: x["TempoEspera"] / x["ChamadasAtendidas"] 
                                if x["ChamadasAtendidas"] > 0 else 0, axis=1)
        chunk["% Transferência"] = chunk.apply(lambda x: (x["ChamadasTransferidas"] / x["ChamadasAtendidas"]) * 100 
                                            if x["ChamadasAtendidas"] > 0 else 0, axis=1)
        
        # Remove colunas desnecessárias
        chunk.drop(columns=["TempoFaladoTotal", "TempoEspera", "ChamadasTransferidas"], inplace=True)
        
        return chunk
    except Exception as e:
        print(f"❌ Erro ao processar chunk: {e}")
        raise

def tratar_hsplit(arquivo_entrada, pasta_saida="data/process"):
    """Processa o arquivo HSPLIT.csv para otimizar os KPIs necessários."""
    try:
        os.makedirs(pasta_saida, exist_ok=True)
        print(f"\nProcessando arquivo: {arquivo_entrada}")
        
        # Verifica se o arquivo existe
        if not os.path.exists(arquivo_entrada):
            print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
            return False
            
        # Lê o arquivo em chunks para economizar memória
        chunks = []
        for chunk in pd.read_csv(arquivo_entrada, chunksize=50000, low_memory=False):
            # Processa cada chunk
            chunk_processado = processar_chunk_hsplit(chunk)
            chunks.append(chunk_processado)
        
        # Concatena todos os chunks
        df = pd.concat(chunks, ignore_index=True)
        
        # Salva arquivo
        arquivo_saida = os.path.join(pasta_saida, "HSPLIT.csv")
        print(f"Salvando arquivo em: {arquivo_saida}")
        print(f"Dimensões finais do DataFrame: {df.shape}")
        df.to_csv(arquivo_saida, index=False, encoding="utf-8")
        
        print("✅ Arquivo processado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao processar HSPLIT.csv: {e}")
        logging.error(f"Erro ao processar HSPLIT.csv: {e}")
        return False

def processar_arquivos_grandes():
    """Processa arquivos CSV com mais de 266 colunas na pasta process"""
    logging.info("Iniciando processamento de arquivos grandes...")
    
    pasta_process = "data/process"
    try:
        # Lista todos os arquivos CSV na pasta process
        arquivos_csv = glob.glob(os.path.join(pasta_process, "*.csv"))
        
        for arquivo in arquivos_csv:
            try:
                nome_arquivo = os.path.basename(arquivo)
                
                if nome_arquivo.startswith('HSPLIT'):
                    # Processa HSPLIT com a nova função
                    if tratar_hsplit(arquivo, pasta_process):
                        os.remove(arquivo)  # Remove o arquivo original apenas se o processamento foi bem sucedido
                        logging.info("Arquivo HSPLIT processado com novos KPIs")
                    
                elif nome_arquivo.startswith('HAGENT'):
                    # Processa HAGENT com a nova função
                    if tratar_hagent(arquivo, pasta_process):
                        os.remove(arquivo)  # Remove o arquivo original apenas se o processamento foi bem sucedido
                        logging.info("Arquivo HAGENT processado com novos KPIs")
                    
            except Exception as e:
                logging.error(f"Erro ao processar arquivo {nome_arquivo}: {e}")
                
    except Exception as e:
        logging.error(f"Erro no processamento de arquivos grandes: {e}")

def mover_para_backup(arquivo):
    """Move arquivo para pasta de backup ao invés de deletar"""
    try:
        pasta_backup = "data/backup"
        os.makedirs(pasta_backup, exist_ok=True)
        nome_backup = f"{os.path.splitext(os.path.basename(arquivo))[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        shutil.move(arquivo, os.path.join(pasta_backup, nome_backup))
        logging.info(f"Arquivo movido para backup: {nome_backup}")
    except Exception as e:
        logging.error(f"Erro ao fazer backup do arquivo {arquivo}: {e}")

def main():
    """Fluxo principal de execução do script."""
    try:
        logging.info("Iniciando processo de extração e tratamento...")
        
        # Baixa arquivos do Kaggle
        baixar_arquivo_kangle()
        
        # Extrai arquivos do ZIP
        extrair_e_mover_arquivos()
        
        # Processa os arquivos XLSX para CSV
        processar_arquivos_raw()
        
        # Baixa arquivos da API
        for nome, url in URLS_APIS.items():
            baixar_arquivo_api(nome, url)
        
        # Processa os arquivos da API
        processar_forecast()
        processar_depara_skill()
        
        # Concatena os arquivos HSPLIT e HAGENT
        concatenar_arquivos()
        
        # Remove duplicatas
        remover_duplicatas_process()
        
        # Processa e otimiza os arquivos grandes
        processar_arquivos_grandes()
        
        logging.info("Processo concluído com sucesso!")
        
    except Exception as e:
        logging.error(f"Erro no processo principal: {e}")

if __name__ == "__main__":
    main()
