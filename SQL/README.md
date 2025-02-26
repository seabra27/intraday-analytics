# Documentação dos Scripts SQL - Projeto Intraday

Este repositório contém uma série de scripts SQL para criação e gerenciamento de um banco de dados de análise Intraday. Abaixo está a descrição de cada arquivo e sua função:

## Estrutura dos Arquivos

### 1. 01_Criacao_Banco.sql
- Script responsável pela criação do banco de dados BD_INTRADAY
- Este é o primeiro script que deve ser executado

### 2. 02_Criacao_Tabelas.sql
- Cria as estruturas das tabelas principais do sistema:
  - DEPARA_SKILL: Tabela de mapeamento de skills e operações
  - FORECAST: Tabela de previsões e métricas planejadas
  - HAGENT: Tabela de métricas dos agentes (tempo logado, pausas)
  - HSPLIT: Tabela de métricas de chamadas e atendimento

### 3. 03_Carga_Dados_Bulk_Insert.sql
- Realiza a importação em massa (bulk insert) dos dados a partir de arquivos CSV
- Configura os parâmetros de importação como:
  - Codificação UTF-8
  - Separador de campos (vírgula)
  - Ignora primeira linha (cabeçalho)

### 4. 04_Stored_Procedures.sql
Contém as procedures para tratamento e limpeza dos dados:
- sp_Tratamento_FORECAST: Trata dados da tabela FORECAST
- sp_Tratamento_DEPARA_SKILL: Trata dados da tabela DEPARA_SKILL
- sp_Tratamento_HAGENT: Trata dados da tabela HAGENT
- sp_Tratamento_HSPLIT: Trata dados da tabela HSPLIT

Principais tratamentos realizados:
- Remoção de espaços em branco
- Correção de formatos de data
- Eliminação de duplicatas
- Tratamento de valores nulos ou inconsistentes

### 5. 05_Views_PowerBI.sql
Cria views otimizadas para consumo no Power BI:
- vw_DEPARA_SKILL: View da tabela DEPARA_SKILL
- vw_FORECAST: View da tabela FORECAST
- vw_HAGENT: View da tabela HAGENT
- vw_HSPLIT: View da tabela HSPLIT

### 6. 06_Verificacoes_Finais.sql
Script para validação da qualidade dos dados:
- Contagem total de registros por tabela
- Verificação de valores nulos em colunas críticas
- Identificação de registros duplicados
- Amostragem de dados para inspeção manual

## Ordem de Execução
Para correta implementação do banco de dados, execute os scripts na ordem numérica:
1. 01_Criacao_Banco.sql
2. 02_Criacao_Tabelas.sql
3. 03_Carga_Dados_Bulk_Insert.sql
4. 04_Stored_Procedures.sql
5. 05_Views_PowerBI.sql
6. 06_Verificacoes_Finais.sql