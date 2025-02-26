--CRIAÇÃO TABELA DEPARA_SKILL
CREATE TABLE DEPARA_SKILL (
    id VARCHAR(50) PRIMARY KEY,  
    CH_Minutos INT,
    OPERACOES_FORECAST VARCHAR(255),
    INI_VIGENCIA DATE,
    CH INT,
    GRUPO VARCHAR(255),
    Consolidado VARCHAR(255),
    ACD INT,
    SEGMENTOS_CALCULADORA_FIN VARCHAR(255),
    DUMMY INT,
    SERVIDOR VARCHAR(255),
    OPERACOES VARCHAR(255),
    SKILL INT,
    SEGMENTOS VARCHAR(255),
    FIM_VIGENCIA DATE,
    ALTERACAO VARCHAR(255),
    CHAMADO VARCHAR(255)
);

--CRIAÇÃO TABELA FORECAST
CREATE TABLE FORECAST (
    id VARCHAR(50) PRIMARY KEY,
    VOLUME_OFERECIDAS FLOAT,
    PERDA_DE_LOG INT,
    CLIENTE VARCHAR(255),
    HC_PREVISTO_S_INDISP FLOAT,
    NS_PREVISTO FLOAT,
    REUNIAO INT,
    NR17 FLOAT,
    HC_BRUTO FLOAT,
    VOLUME_ATENDIDAS FLOAT,
    TREINAMENTO FLOAT,
    TC_ID INT,
    GRUPO VARCHAR(255),
    FEEDBACK INT,
    OPERAÇÃO_PUNCH VARCHAR(255),
    TMO_PREVISTO FLOAT,
    ABS INT,
    PRODUTO VARCHAR(255),
    SISTEMA FLOAT,
    SITE VARCHAR(255),
    DATA DATE,
    CELULA VARCHAR(255),
    BANHEIRO FLOAT,
    INTERVALO VARCHAR(255)
);

--CRIAÇÃO TABELA HAGENT
DROP TABLE IF EXISTS HAGENT;
CREATE TABLE HAGENT (
    Data DATE,
    TempoLogado FLOAT,
    Pausas FLOAT,
    Pausas_NR17 FLOAT,
    Outras_Pausas FLOAT,
    Ocupação FLOAT
);


--CRIAÇÃO TABELA HSPLIT
CREATE TABLE HSPLIT (
    Data DATE,
    ChamadasRecebidas FLOAT,
    ChamadasAtendidas FLOAT,
    ChamadasAtendidasNs FLOAT,
    AbandonadasNs FLOAT,
    NS FLOAT,
    TMA FLOAT,
    TME FLOAT,
    Transferencia FLOAT
);