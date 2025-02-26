# Pipeline de Extração e Processamento de Dados

Este projeto implementa um pipeline automatizado para extração, transformação e processamento de dados de diferentes fontes, incluindo Kaggle e APIs Airtable.

## Estrutura do Projeto

├── data/
│ ├── raw/ # Dados brutos baixados
│ ├── process/ # Dados processados
│ 
├── main.py # Script principal
├── requirements.txt # Dependências do projeto
├── .env # Variáveis de ambiente
└── log_extracao.log # Arquivo de logs/ Criado ao executar o script
```

## Pré-requisitos

- Python 3.9.5+
- Bibliotecas Python listadas em `requirements.txt`
- Credenciais do Kaggle configuradas no `.env`
- Token de acesso da API Airtable no `.env`

## Configuração do Ambiente

1. Certifique-se de ter o Python 3.9.5 ou superior instalado:
```bash
python --version
```

2. Crie e ative um ambiente virtual:

No Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

No Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` com as seguintes variáveis:
```
KAGGLE_EMAIL=seu_email
KAGGLE_PASSWORD=sua_senha
BEARER_TOKEN=seu_token_airtable
```

## Requirements.txt

O projeto utiliza as seguintes bibliotecas principais:
```
pandas==2.0.0
numpy==1.24.3
selenium==4.9.0
requests==2.28.2
python-dotenv==1.0.0
openpyxl==3.1.2
```

## Fluxo de Execução

O pipeline executa as seguintes etapas:

### 1. Extração de Dados

#### Download do Kaggle
- Automatiza login no Kaggle via Selenium
- Baixa dataset de volumetria
- Extrai arquivos ZIP para pasta `raw/`

#### Download das APIs
- Faz requisições para APIs do Airtable
- Baixa dados de forecast e mapeamento de skills
- Salva arquivos CSV na pasta `process/`

### 2. Processamento Inicial

#### Conversão de Formatos
- Converte arquivos XLSX para CSV
- Normaliza dados JSON das APIs
- Remove caracteres especiais

#### Concatenação de Arquivos
- Agrupa arquivos HSPLIT por data
- Agrupa arquivos HAGENT por data
- Mantém versões mais recentes

### 3. Tratamento de Dados

#### Limpeza
- Remove duplicatas
- Otimiza tipos de dados
- Trata valores nulos

#### Cálculo de KPIs

Para arquivos HSPLIT:
- Nível de Serviço (NS)
- Tempo Médio de Atendimento (TMA) 
- Tempo Médio de Espera (TME)
- % de Transferência

Para arquivos HAGENT:
- % de Pausas
- % Pausas NR17
- % Outras Pausas
- % Ocupação

### 4. Finalização

- Move arquivos processados para backup
- Gera logs detalhados
- Limpa arquivos temporários

## Funções Principais

- `baixar_arquivo_kangle()`: Automatiza download do Kaggle
- `baixar_arquivo_api()`: Faz download das APIs
- `processar_arquivos_raw()`: Processa arquivos brutos
- `concatenar_arquivos()`: Agrupa arquivos por tipo
- `tratar_hsplit()`: Calcula KPIs de atendimento
- `tratar_hagent()`: Calcula KPIs de agentes
- `remover_duplicatas_process()`: Remove registros duplicados
- `processar_arquivos_grandes()`: Otimiza arquivos extensos

## Logs

O sistema gera logs detalhados em `log_extracao.log` com:

- Início/fim de cada etapa
- Erros e exceções
- Métricas de processamento
- Alertas e avisos

## Execução

Para executar o pipeline:

```bash
python main.py
```

## Tratamento de Erros

O sistema possui tratamento robusto de erros:

- Validação de credenciais
- Verificação de arquivos
- Backup antes de alterações
- Logs detalhados de falhas

## Otimizações

- Processamento em chunks para arquivos grandes
- Otimização de tipos de dados
- Remoção de colunas desnecessárias
- Backup automático

## Manutenção

- Verifique logs regularmente
- Monitore uso de memória
- Atualize credenciais quando necessário
- Faça backup dos dados processados