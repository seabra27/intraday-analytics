-- Procedure de Tratamento da Tabela FORECAST
CREATE PROCEDURE sp_Tratamento_FORECAST
AS
BEGIN
    SET NOCOUNT ON;

    -- Remover espaços em branco de colunas de texto
    UPDATE FORECAST
    SET 
        id = LTRIM(RTRIM(id)),
        CLIENTE = LTRIM(RTRIM(CLIENTE)),
        GRUPO = LTRIM(RTRIM(GRUPO)),
        OPERAÇÃO_PUNCH = LTRIM(RTRIM(OPERAÇÃO_PUNCH)),
        PRODUTO = LTRIM(RTRIM(PRODUTO)),
        SITE = LTRIM(RTRIM(SITE)),
        CELULA = LTRIM(RTRIM(CELULA)),
        INTERVALO = LTRIM(RTRIM(INTERVALO));

    -- Remover registros com `id` nulo ou vazio (se necessário)
    DELETE FROM FORECAST WHERE id IS NULL OR id = '';

    -- Corrigir formatação da coluna `DATA`
    UPDATE FORECAST
    SET DATA = TRY_CONVERT(DATE, DATA, 103)
    WHERE DATA IS NOT NULL;

    -- Remover possíveis duplicatas
    WITH CTE AS (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY DATA) AS rn
        FROM FORECAST
    )
    DELETE FROM CTE WHERE rn > 1;
END;
GO  -- <=== Separação necessária para evitar erro de sintaxe

--Execução de Procedure Tabela FORECAST
EXEC sp_Tratamento_FORECAST;
GO
--------------------------------------------------------

-- Procedure de Tratamento da Tabela DEPARA_SKILL
CREATE PROCEDURE sp_Tratamento_DEPARA_SKILL
AS
BEGIN
    SET NOCOUNT ON;

    -- Remover espaços em branco de colunas de texto
    UPDATE DEPARA_SKILL
    SET 
        OPERACOES_FORECAST = LTRIM(RTRIM(OPERACOES_FORECAST)),
        GRUPO = LTRIM(RTRIM(GRUPO)),
        Consolidado = LTRIM(RTRIM(Consolidado)),
        SERVIDOR = LTRIM(RTRIM(SERVIDOR)),
        OPERACOES = LTRIM(RTRIM(OPERACOES)),
        SEGMENTOS_CALCULADORA_FIN = LTRIM(RTRIM(SEGMENTOS_CALCULADORA_FIN)),
        SEGMENTOS = LTRIM(RTRIM(SEGMENTOS));

    -- Remover registros com `id` nulo ou vazio
    DELETE FROM DEPARA_SKILL WHERE id IS NULL OR id = '';

    -- Corrigir formatação das colunas de data
    UPDATE DEPARA_SKILL
    SET INI_VIGENCIA = TRY_CONVERT(DATE, INI_VIGENCIA, 103)
    WHERE INI_VIGENCIA IS NOT NULL;

    UPDATE DEPARA_SKILL
    SET FIM_VIGENCIA = TRY_CONVERT(DATE, FIM_VIGENCIA, 103)
    WHERE FIM_VIGENCIA IS NOT NULL;

    -- Remover possíveis registros duplicados
    WITH CTE AS (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY INI_VIGENCIA) AS rn
        FROM DEPARA_SKILL
    )
    DELETE FROM CTE WHERE rn > 1;
END;
GO

--Execução da Procedure
EXEC sp_Tratamento_DEPARA_SKILL;
GO
--------------------------------------------------------

-- Procedure de Tratamento da Tabela HAGENT
CREATE PROCEDURE sp_Tratamento_HAGENT
AS
BEGIN
    SET NOCOUNT ON;

    -- Corrigir formatação da coluna `Data`
    UPDATE HAGENT
    SET Data = TRY_CONVERT(DATE, Data, 103)
    WHERE Data IS NOT NULL;

    -- Remover registros com `Data` nula (se necessário)
    DELETE FROM HAGENT WHERE Data IS NULL;

    -- Substituir valores negativos ou inconsistentes por NULL
    UPDATE HAGENT
    SET TempoLogado = NULL WHERE TempoLogado < 0;

    UPDATE HAGENT
    SET Pausas = NULL WHERE Pausas < 0;

    UPDATE HAGENT
    SET Pausas_NR17 = NULL WHERE Pausas_NR17 < 0;

    UPDATE HAGENT
    SET Outras_Pausas = NULL WHERE Outras_Pausas < 0;

    UPDATE HAGENT
    SET Ocupação = NULL WHERE Ocupação < 0;

    -- Remover possíveis registros duplicados
    WITH CTE AS (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY Data, TempoLogado ORDER BY Data) AS rn
        FROM HAGENT
    )
    DELETE FROM CTE WHERE rn > 1;
END;
GO

--Execução de Procedure
EXEC sp_Tratamento_HAGENT;
GO
--------------------------------------------------------

-- Procedure de Tratamento da Tabela HSPLIT
CREATE PROCEDURE sp_Tratamento_HSPLIT
AS
BEGIN
    SET NOCOUNT ON;

    -- Corrigir formatação da coluna `Data`
    UPDATE HSPLIT
    SET Data = TRY_CONVERT(DATE, Data, 103)
    WHERE Data IS NOT NULL;

    -- Remover registros com `Data` nula
    DELETE FROM HSPLIT WHERE Data IS NULL;

    -- Substituir valores negativos ou inconsistentes por NULL
    UPDATE HSPLIT
    SET ChamadasRecebidas = NULL WHERE ChamadasRecebidas < 0;

    UPDATE HSPLIT
    SET ChamadasAtendidas = NULL WHERE ChamadasAtendidas < 0;

    UPDATE HSPLIT
    SET ChamadasAtendidasNs = NULL WHERE ChamadasAtendidasNs < 0;

    UPDATE HSPLIT
    SET AbandonadasNs = NULL WHERE AbandonadasNs < 0;

    UPDATE HSPLIT
    SET NS = NULL WHERE NS < 0;

    UPDATE HSPLIT
    SET TMA = NULL WHERE TMA < 0;

    UPDATE HSPLIT
    SET TME = NULL WHERE TME < 0;

    UPDATE HSPLIT
    SET Transferencia = NULL WHERE Transferencia < 0;

    -- Remover possíveis registros duplicados
    WITH CTE AS (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY Data, ChamadasRecebidas ORDER BY Data) AS rn
        FROM HSPLIT
    )
    DELETE FROM CTE WHERE rn > 1;
END;
GO

--Execução Procedure
EXEC sp_Tratamento_HSPLIT;
GO
