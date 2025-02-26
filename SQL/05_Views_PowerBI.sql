--Criação de View Tabela DEPARA_SKILL
CREATE VIEW vw_DEPARA_SKILL AS
SELECT 
    id, 
    CH_Minutos, 
    OPERACOES_FORECAST, 
    INI_VIGENCIA, 
    CH, 
    GRUPO, 
    Consolidado, 
    ACD, 
    SEGMENTOS_CALCULADORA_FIN, 
    DUMMY, 
    SERVIDOR, 
    OPERACOES, 
    SKILL, 
    SEGMENTOS, 
    FIM_VIGENCIA, 
    ALTERACAO, 
    CHAMADO
FROM DEPARA_SKILL
WHERE INI_VIGENCIA IS NOT NULL;
GO  
---------------------------------------------------------
--Criação de View Tabela FORECAST
CREATE VIEW vw_FORECAST AS
SELECT 
    id, 
    DATA, 
    CLIENTE, 
    GRUPO, 
    VOLUME_OFERECIDAS, 
    VOLUME_ATENDIDAS, 
    NS_PREVISTO, 
    TMO_PREVISTO
FROM FORECAST
WHERE DATA IS NOT NULL;
GO
---------------------------------------------------------
--Criação de View Tabela HAGENT
CREATE VIEW vw_HAGENT AS
SELECT 
    Data, 
    TempoLogado, 
    Pausas, 
    Pausas_NR17, 
    Outras_Pausas, 
    Ocupação
FROM HAGENT;
GO
---------------------------------------------------------
--Criação de View Tabela HSPLIT
CREATE VIEW vw_HSPLIT AS
SELECT 
    Data, 
    ChamadasRecebidas, 
    ChamadasAtendidas, 
    ChamadasAtendidasNs, 
    AbandonadasNs, 
    NS, 
    TMA, 
    TME, 
    Transferencia
FROM HSPLIT;
GO

--Verificação de Criação das Views
SELECT TOP 10 * FROM vw_FORECAST;
SELECT TOP 10 * FROM vw_HAGENT;
SELECT TOP 10 * FROM vw_HSPLIT;
SELECT TOP 10 * FROM vw_DEPARA_SKILL;
