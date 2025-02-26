--Importação de dados - DEPARA_SKILL.csv
BULK INSERT DEPARA_SKILL
FROM 'C:\prova_pedro_seabra_neobpo_30012025\data\process\DEPARA_SKILL.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,  -- Ignorar cabeçalho
    FIELDTERMINATOR = ',', -- Separação por vírgula
    ROWTERMINATOR = '0x0A', -- Quebra de linha padrão
    CODEPAGE = '65001', -- Para arquivos em UTF-8
    TABLOCK
);

--Importação de dados - FORECAST.csv
BULK INSERT FORECAST
FROM 'C:\prova_pedro_seabra_neobpo_30012025\data\process\FORECAST.csv'
WITH (
    FIRSTROW = 2,  -- Ignorar cabeçalho
    FIELDTERMINATOR = ',', -- Separação por vírgula
    ROWTERMINATOR = '0x0A', -- Quebra de linha padrão
    CODEPAGE = '65001', -- UTF-8
    TABLOCK
);


--Importação de dados - HAGENT.csv
BULK INSERT HAGENT
FROM 'C:\prova_pedro_seabra_neobpo_30012025\data\process\HAGENT.csv'
WITH (
    FIRSTROW = 2,  -- Ignorar cabeçalho
    FIELDTERMINATOR = ',', -- Separação por vírgula
    ROWTERMINATOR = '0x0A', -- Quebra de linha padrão
    CODEPAGE = '65001', -- UTF-8
    TABLOCK
);


--Importação de dados - HSPLIT.csv
BULK INSERT HSPLIT
FROM 'C:\prova_pedro_seabra_neobpo_30012025\data\process\HSPLIT.csv'
WITH (
    FIRSTROW = 2,  -- Ignorar cabeçalho
    FIELDTERMINATOR = ',', -- Separação por vírgula
    ROWTERMINATOR = '0x0A', -- Quebra de linha padrão
    CODEPAGE = '65001', -- UTF-8
    TABLOCK
);