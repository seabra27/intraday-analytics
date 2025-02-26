# 📊 Relatório Intraday - Power BI, Python e SQL

## 📌 Visão Geral

Este projeto apresenta uma solução para monitoramento em tempo real de indicadores operacionais, incluindo volumetria de chamadas telefônicas, tempos de atendimento e métricas de produtividade. A abordagem integra a extração automatizada de dados, processamento e armazenamento eficiente, além de visualizações interativas para análise gerencial.

O desenvolvimento foi estruturado nas seguintes etapas:

1. **Automação da Extração de Dados** - Implementação de scripts em Python para coleta de dados via APIs e web scraping.
2. **Tratamento e Armazenamento** - Processamento e modelagem dos dados no SQL Server.
3. **Visualização e Análise** - Construção de dashboards interativos no Power BI.

---

## 🚀 Tecnologias Utilizadas

- **Python**: Selenium, Pandas, Requests, dotenv, OpenPyXL, NumPy
- **SQL Server**: BULK INSERT, Procedures, Normalização, Views otimizadas para análise
- **Power BI**: DAX, Visuais Interativos, KPIs, Comparação Forecast x Real

---

## 📂 Estrutura do Repositório

```
📂 intraday_project
│── 📂 Python
│   ├── main.py                     # Script principal para automação
│   ├── extracao_dados.py           # Extração de dados via web scraping e API
│   ├── conversao_csv.py            # Conversão de arquivos .xlsx para .csv
│   ├── automacao_login.py          # Automação de login e download de arquivos
│   ├── requirements.txt            # Dependências do projeto
│   ├── .env                        # Configuração de variáveis de ambiente
│   ├── log_extracao.log            # Logs de execução
│   ├── README.md                   # Documentação do pipeline
│
│── 📂 SQL
│   ├── 01_Criacao_Banco.sql        # Criação do banco de dados
│   ├── 02_Criacao_Tabelas.sql      # Estruturação das tabelas
│   ├── 03_Carga_Dados_Bulk_Insert.sql # Importação de dados CSV
│   ├── 04_Stored_Procedures.sql    # Procedures de tratamento de dados
│   ├── 05_Views_PowerBI.sql        # Views otimizadas para consumo no Power BI
│   ├── 06_Verificacoes_Finais.sql  # Validações de integridade dos dados
│   ├── README.md                   # Documentação dos scripts SQL
│
│── 📂 PowerBI
│   ├── relatorio_intraday.pbix     # Dashboard interativo
│   ├── README.md                   # Explicação sobre a estrutura do dashboard
│
│── 📂 Documentacao
│   ├── desafio.pdf                  # Documento original do desafio (Se permitido)
│   ├── instrucoes.md                 # Informações sobre a proposta e abordagem
│
│── README.md                         # Documentação principal
│── .gitignore                         # Arquivos ignorados no versionamento
│── LICENÇA.md                        # Licença do projeto (Opcional)
```

---

## 🛠️ Execução do Projeto

### 1️⃣ **Configuração do Ambiente Python**

```bash
pip install -r Python/requirements.txt
```

### 2️⃣ **Execução da Extração de Dados**

```bash
python Python/main.py
```

### 3️⃣ **Processamento e Armazenamento no SQL Server**

- **Criação do banco e tabelas**:
  ```sql
  EXEC 01_Criacao_Banco.sql;
  EXEC 02_Criacao_Tabelas.sql;
  ```
- **Carga de dados**:
  ```sql
  EXEC 03_Carga_Dados_Bulk_Insert.sql;
  ```
- **Execução das procedures para tratamento dos dados**:
  ```sql
  EXEC 04_Stored_Procedures.sql;
  ```
- **Criação das views para análise no Power BI**:
  ```sql
  EXEC 05_Views_PowerBI.sql;
  ```

### 4️⃣ **Visualização no Power BI**

- Abrir `PowerBI/relatorio_intraday.pbix` no Power BI.
- Atualizar as fontes de dados.
- Explorar as análises disponíveis.

---

## 📊 Análises Disponíveis no Dashboard

O dashboard interativo foi projetado para fornecer insights estratégicos sobre a operação, destacando os seguintes indicadores:

- **Volumetria de Chamadas**: Chamadas Recebidas, Atendidas e Abandonadas
- **Nível de Serviço (NS)**: Comparação entre valores reais e planejados
- **Tempo Médio de Atendimento (TMA)** e **Tempo Médio de Espera (TME)**
- **Ocupação e Pausas dos Agentes**
- **Análise Temporal**: Comparação intradiária, diária, semanal e mensal

### 🔍 Principais Funcionalidades
- Design responsivo para facilitar a interpretação dos dados
- Comparação dinâmica entre previsões e resultados reais
- Indicadores detalhados de produtividade e eficiência operacional
- Gráficos intradiários para análise granular dos períodos de maior impacto

---

## 📜 Licença

Este projeto é disponibilizado sob a licença MIT. Para mais detalhes, consulte [LICENÇA.md](LICENÇA.md).

---

## 📩 Contato

Para dúvidas ou sugestões, entre em contato:

📩 Email: pedroseabra2701@gmail.com

🌐 LinkedIn: https://linkedin.com/in/seu-perfil)](https://www.linkedin.com/in/pedro-silva-seabra-de-oliveira


