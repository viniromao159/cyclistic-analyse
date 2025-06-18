# Análise de compartilhamento de bicicletas - Cyclistic

### 1. Introdução

Neste estudo de caso, trabalho como analista de dados júnior em uma empresa fictícia chamada Cyclistic. O diretor de marketing acredita que o sucesso futuro da empresa depende da maximização do número de assinaturas anuais.

Portanto, a minha equipe quer entender como os ciclistas casuais e os membros anuais usam as bicicletas Cyclistic de forma diferente com o objetivo de gerar novos insights para uma nova estratégia de marketing de conversão dos ciclistas casuais para membros anuais.

---

#### Perguntas

1. Como os membros anuais e os ciclistas casuais usam as bicicletas Cyclistic de maneira diferente?
2. Por que ciclistas casuais comprariam assinaturas anuais da Cyclistic?
3. Como a Cyclistic pode usar a mídia digital para influenciar ciclistas casuais a se tornarem membros?

#### Objetivo

O projeto tem como propósito realizar uma análise exploratória sobre os dados de viagens das bicicletas alugáveis da Cyclistic com a finalidade de responder a diferença de uso do produto entre membros anuais e ciclistas casuais.

Criar um relatório que responde a pergunta:
**Como os membros anuais e os ciclistas casuais usam as bicicletas Cyclistic de forma diferente?**

---

### 2. Preparação

**Fonte dos dados:**
[Index of bucket "divvy-tripdata"](https://divvy-tripdata.s3.amazonaws.com/index.html)

**Período analisado:** 01/2024 - 12/2024
**Total de arquivos:** 12 (1 por mês)
**Formato:** CSV
**Armazenamento inicial:** Local  
**Armazenamento final:** [Github](https://github.com/viniromao159/cyclistic-analyse.git)

#### Estrutura dos arquivos

Os arquivos CSV contêm as seguintes colunas:

| Coluna             | Descrição                                         |
| ------------------ | ------------------------------------------------- |
| ride_id            | Identificador da viagem.                          |
| rideable_type      | Tipo da bicicleta utilizada na viajem.            |
| started_at         | Data e hora do inicio da viagem.                  |
| ended_at           | Data e hora do fim da viagem.                     |
| start_station_name | Nome da estação de coleta da bicicleta            |
| start_station_id   | Identificador da estação de coleta da bicicleta.  |
| end_station_name   | Nome da estação de entrega da bicicleta           |
| end_station_id     | Identificador da estação de entrega da bicicleta. |
| start_lat          | Latitude do local de coleta.                      |
| start_lng          | Longitude do local de coleta.                     |
| end_lat            | Latitude do local de entrega.                     |
| end_lng            | Longitude do local de coleta.                     |
| member_casual      | Tipo de usuário da viagem (Membro/causal).        |

---

### 3. Processamento

#### Ferramentas

Na escolha das ferramentas, considerei inicialmente a utilização de amostra dos dados para utilização de planilhas, porém optei a não utiliza-la devido a alta quantidade de dados.
A ferramenta selecionada foi o SQL para realizar o processo de limpeza, tratamento dos dados e análise.

Ferramentas utilizadas no projeto:

- **PostgreSQL/pgAdmin**: para armazenamento, limpeza, transformação dos dados e análise dos dados.

#### Carga dos dados

Optei por utilizar o **PostgreSQL**, por ser um sistema robusto e compatível com SQL padrão. A carga foi realizada utilizando a ferramenta **pgAdmin** seguindo o padrão abaixo:

Código SQL:

```bash
CREATE TABLE public."202406-divvy-tripdata"
(
    ride_id TEXT,
    rideable_type TEXT,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    start_station_name TEXT,
    start_station_id TEXT,
    end_station_name TEXT,
    end_station_id TEXT,
    start_lat NUMERIC,
    start_lng NUMERIC,
    end_lat NUMERIC,
    end_lng NUMERIC,
    member_casual TEXT
);
```

Arquivo: Criação das tabelas

Padronizei a importação através das ferramentas do **pgAdmin** para evitar conflitos. A configuração das importação das tabelas foram como o exemplo abaixo:

- CSVs importados com cabeçalho e delimitador `,`.
- Inclusão de cabeçalho na primeira linha;

![image.png](img/image%201.png)

#### Tratamento dos dados

**Criação da tabela consolidada para análise**

Dado que os dados coletados estão distribuídos em 12 arquivos CSV com a mesma estrutura, optei por consolidar todos os dados em uma única tabela para facilitar o processo de limpeza, tratamento e análise através do SQL.
A nova tabela chamada `year_tripdata` foi criada utilizando o comando `UNION ALL`, para empilhamento dos dados mantendo a estrutura original.

Os benefícios dessa abordagem são:

- Centralização dos dados
- Eficiência nos processos
- Segurança dos dados originais nas suas tabelas de origem

Código SQL:

```bash
CREATE TABLE year_tripdata AS
SELECT * FROM public."202401-divvy-tripdata"
UNION ALL
SELECT * FROM public."202402-divvy-tripdata"
UNION ALL
SELECT * FROM public."202403-divvy-tripdata"
UNION ALL
SELECT * FROM public."202404-divvy-tripdata"
UNION ALL
SELECT * FROM public."202405-divvy-tripdata"
UNION ALL
SELECT * FROM public."202406-divvy-tripdata"
UNION ALL
SELECT * FROM public."202407-divvy-tripdata"
UNION ALL
SELECT * FROM public."202408-divvy-tripdata"
UNION ALL
SELECT * FROM public."202409-divvy-tripdata"
UNION ALL
SELECT * FROM public."202410-divvy-tripdata"
UNION ALL
SELECT * FROM public."202411-divvy-tripdata"
UNION ALL
SELECT * FROM public."202412-divvy-tripdata";
```

Arquivo: Criação da year_tripdata

**Inclusão de novas colunas**

Foram criadas colunas derivadas de outras já existentes para auxiliarem na segmentação dos dados, no cálculo de métricas e na interpretação dos resultados.

Código SQL:

```bash
ALTER TABLE public.year_tripdata
ADD COLUMN start_date DATE,
ADD COLUMN start_hour TIME,
ADD COLUMN week_start_day TEXT,
ADD COLUMN week_start_day_num INTEGER,
ADD COLUMN ended_date DATE,
ADD COLUMN ended_hour TIME,
ADD COLUMN trip_length INTERVAL;


UPDATE public.year_tripdata
SET
    start_date = DATE(started_at),
    start_hour = started_at::TIME,
    week_start_day = TO_CHAR(started_at, 'Day'),
    week_start_day_num = EXTRACT(DOW FROM started_at)::INTEGER,
    ended_date = DATE(ended_at),
    ended_hour = ended_at::TIME,
    trip_length = ended_at - started_at;
```

Arquivo: Criação das colunas

Abaixo as colunas inseridas com os métodos e sua finalidade:

| Nova Coluna        | Método de Criação                     | Finalidade/Justificativa   | Formatação |
| ------------------ | ------------------------------------- | -------------------------- | ---------- |
| start_date         | DATE(started_at)                      | Data de início da viagem   | DATE       |
| start_date         | started_at::TIME                      | Hora de início da viagem   | TIME       |
| week_start_day     | TO_CHAR(started_at, 'Day')            | Dia da semana              | TEXT       |
| week_start_day_num | EXTRACT(DOW FROM started_at)::INTEGER | Dia da semana (1 - 7)      | INTEGER    |
| ended_date         | DATE(ended_at)                        | Data do fim da viagem      | DATE       |
| ended_hour         | ended_at::TIME                        | Hora do fim da viagem      | TIME       |
| trip_length        | ended_at - started_at                 | Tamanho da viagem em horas | INTERVAL   |

#### Limpeza de dados

Antes de realizar alterações destrutivas na tabela `year_tripdata`, como a exclusão de colunas ou remoção de linhas , foi realizada uma etapa de backup completo da tabela. O comando abaixo criou uma cópia exata da até a etapa atual.

Código SQL:

```bash
CREATE TABLE year_tripdata_backup AS
SELECT * FROM year_tripdata;
```

Arquivo: Criação das colunas

**Remoção de colunas**

Na fase de limpeza, foram identificadas colunas que não contribuíam para os objetivos do projeto. Essas colunas continham informações irrelevantes ou fora do escopo da análise. A opção por remove-las é manter os dados eficiente e focado.

Foram removidas as seguintes colunas:

| Coluna           | Descrição                                        |
| ---------------- | ------------------------------------------------ |
| started_at       | Data e Hora do inicio da viagem                  |
| start_station_id | Identificador da estação de coleta da bicicleta  |
| ended_at         | Data e Hora do fim da viagem                     |
| end_station_id   | Identificador da estação de entrega da bicicleta |
| start_lat        | Latitude do local de coleta                      |
| start_lng        | Longitude do local de coleta                     |
| end_lat          | Latitude do local de entrega                     |
| end_lng          | Longitude do local de coleta                     |

Código SQL:

```bash
ALTER TABLE public.year_tripdata
DROP COLUMN started_at,
DROP COLUMN start_station_id,
DROP COLUMN ended_at,
DROP COLUMN end_station_id,
DROP COLUMN start_lat,
DROP COLUMN start_lng,
DROP COLUMN end_lat,
DROP COLUMN end_lng;
```

Arquivo: Criação das colunas

**Tratamento de nulos**

Para identificar a quantidade de valores nulos em cada coluna do dataset, foi criada uma query que realiza a contagem desses valores por coluna. Utilizei a função de agregação `COUNT(*)` com `FILTER (WHERE ... IS NULL)` para filtragem de valores nulos em cada coluna.

Código SQL:

```bash
SELECT
  COUNT(*) FILTER (WHERE ride_id IS NULL) AS ride_id,
  COUNT(*) FILTER (WHERE rideable_type IS NULL) AS rideable_type,
  COUNT(*) FILTER (WHERE start_station_name IS NULL) AS start_station_name,
  COUNT(*) FILTER (WHERE end_station_name IS NULL) AS end_station_name,
  COUNT(*) FILTER (WHERE member_casual IS NULL) AS member_casual,
  COUNT(*) FILTER (WHERE start_date IS NULL) AS start_date,
  COUNT(*) FILTER (WHERE start_hour IS NULL) AS start_hour,
  COUNT(*) FILTER (WHERE week_start_day IS NULL) AS week_start_day,
  COUNT(*) FILTER (WHERE week_start_day_num IS NULL) AS week_start_day_num,
  COUNT(*) FILTER (WHERE ended_date IS NULL) AS ended_date,
  COUNT(*) FILTER (WHERE ended_hour IS NULL) AS ended_hour,
  COUNT(*) FILTER (WHERE trip_length IS NULL) AS trip_length
FROM year_tripdata;
```

Arquivo: Tratamento de nulos

Os resultados indicaram a presença de valores nulos em algumas colunas, conforme listado abaixo:

![image.png](img/image%208.png)

Para facilitar a análise e evitar problemas em ferramentas de visualização, os valores nulos foram substituídos pelo texto `empty` por meio de uma query de atualização.

Código SQL:

```bash
UPDATE public."year_tripdata"
SET end_station_name = 'empty'
WHERE end_station_name IS NULL;

UPDATE public."year_tripdata"
SET start_station_name = 'empty'
WHERE start_station_name IS NULL;
```

Arquivo: Tratamento de nulos

Os resultados após a atualização indicaram que a não mais presença de valores nulos:

![image.png](img/image%2010.png)

**Remoção de linhas**

Durante a análise exploratória do dataset year_tripdata, foi identificada a presença de registros com valores anômalos de duração de viagem. Especificamente, duas situações foram consideradas inválidas para o contexto da análise:

1. _Duração negativa:_ Viagens em que a data/hora da viagem ocorre antes da data/hora que o início, o que indica erro de registro ou inconsistência no sistema (227 registros).
2. _Duração superior a 24 horas:_ Viagens com duração igual ou superior a 1 dia. Esse comportamento foge ao padrão esperado para o serviço analisado, além de representar menos de 0,1% do total de dados (7596 registros).

Código SQL:

```bash
DELETE FROM year_tripdata
WHERE trip_length < INTERVAL '0 seconds'
   OR trip_length > INTERVAL '1 day'
```

---

### 4. Análise

Essa etapa apresenta as análises realizadas através do SQL, como foram criadas e seus resultados. Importante destacar que todas as QUERY estão no arquivo `Analise.SQL` em formato de `WITH (CTE)`.

#### Media de tempo das viagens

Para entender melhor o comportamento dos usuários, calculei a média de duração das viagens em minutos, separando entre usuários membros e casuais. Utilizei a função `EXTRACT(EPOCH FROM ...)` para transformar o tempo total da viagem em segundos e, em seguida, converti para minutos.

Esse cálculo me ajudou a identificar que os usuários casuais costumam fazer viagens mais longas em comparação aos membros anuais.

Código SQL:

```bash
avg_tripduration AS(
	SELECT
		member_casual,
		ROUND(AVG(EXTRACT(EPOCH FROM trip_length)/60 ), 2) AS avg_tripduration_minutes
	FROM year_tripdata
	GROUP BY member_casual
),
```

Resultado:

![image.png](img/image%2013.png)

#### Bicicletas mais comuns

Também analisei quais tipos de bicicleta são mais utilizados por cada categoria de usuário (membro anual e casual). Para isso, agrupei os dados por tipo de bicicleta e categoria de usuário, e contei o número total de viagens feitas com cada modelo. Depois, utilizei a função `ROW_NUMBER()` para ranquear os modelos mais usados por grupo, o que me permitiu identificar quais bicicletas são preferidas por cada perfil. Esse ranking foi importante para observar, por exemplo, que o modelo _electric scooters_ são muito mais populares entre os casuais do que entre os membros.

Código SQL:

```bash
bike_count AS (
  SELECT
    member_casual,
    rideable_type,
    COUNT(*) AS total
  FROM year_tripdata
  GROUP BY member_casual, rideable_type
),

common_bikes AS(
	SELECT
		member_casual,
		rideable_type,
		total,
		ROW_NUMBER() OVER(PARTITION BY member_casual ORDER BY total DESC) AS bike_rank
	FROM bike_count
),
```

Resultado:

![image.png](img/image%2015.png)

#### Estações de inicio mais comuns

Para entender os padrões de início das viagens, analisei as estações mais utilizadas como ponto de partida por cada tipo de usuário. Filtrei os dados para considerar apenas estações válidas e depois agrupei por estação e categoria (membro e casual), contando quantas viagens começaram em cada uma. Com o `ROW_NUMBER()`, criei um ranking e selecionei as 5 estações mais populares entre usuários membros e usuários casuais. Essa análise me ajudou a perceber um padrão geográfico interessante: membros tendem a iniciar viagens no centro de Chicago, enquanto os casuais preferem estações próximas a áreas de lazer as margens do Lago Michigan.

Código SQL:

```bash
start_station_count AS (
  SELECT
    member_casual,
    start_station_name,
    COUNT(*) AS total
  FROM year_tripdata
  WHERE start_station_name != 'empty'
  GROUP BY member_casual, start_station_name
),

common_start_stations AS(
	SELECT
		member_casual,
		start_station_name,
		total,
		ROW_NUMBER() OVER(PARTITION BY member_casual ORDER BY total DESC) AS station_rank
	FROM start_station_count
),

top5_start_stations AS (
  SELECT *
  FROM common_start_stations
  WHERE station_rank <= 5
),
```

Resultado:

![image.png](img/image%2017.png)

#### Estações de entregas mais comuns

Além dos pontos de partida, também analisei as estações mais comuns para encerramento das viagens. Filtrei os dados para considerar apenas estações válidas, agrupei por nome da estação e tipo de usuário, e contei quantas vezes cada uma foi usada como destino. Com o uso do `ROW_NUMBER()`, ranqueei as estações mais utilizadas por membros e casuais, selecionando as top 5 para cada grupo. Essa análise reforçou o padrão já observado nas estações de início: membros encerram viagens principalmente na região central, enquanto casuais finalizam em locais mais voltados ao lazer.

Código SQL:

```bash
end_station_count AS (
  SELECT
    member_casual,
    end_station_name,
    COUNT(*) AS total
  FROM year_tripdata
  WHERE end_station_name != 'empty'
  GROUP BY member_casual, end_station_name
),

common_end_stations AS(
	SELECT
		member_casual,
		end_station_name,
		total,
		ROW_NUMBER() OVER(PARTITION BY member_casual ORDER BY total DESC) AS station_rank
	FROM end_station_count
),

top5_end_stations AS (
  SELECT *
  FROM common_end_stations
  WHERE station_rank <= 5
),
```

Resultado:

![image.png](img/image%2019.png)

#### Dias das semanas mais comuns

Também explorei quais dias da semana concentram mais viagens, separando por tipo de usuário. Agrupei os dados pelo dia da semana de início da viagem e pela categoria do usuário, contabilizando o total de viagens em cada combinação. Depois usei `ROW_NUMBER()` para ranquear os dias mais comuns para cada grupo. Essa análise revelou um padrão interessante: usuários membros viajam majoritariamente durante a semana, enquanto os casuais são mais ativos aos finais de semana — reforçando reforça a ideia de que membros usam o serviço para deslocamento diário e os casuais para lazer.

Código SQL:

```bash
week_days_count AS (
  SELECT
    member_casual,
    week_start_day,
    COUNT(*) AS total
  FROM year_tripdata
  GROUP BY member_casual, week_start_day
),

common_week_days AS(
	SELECT
		member_casual,
		week_start_day,
		total,
		ROW_NUMBER() OVER(PARTITION BY member_casual ORDER BY total DESC) AS week_day_rank
	FROM week_days_count
),
```

Resultado:

![image.png](img/image%2021.png)

#### Meses com mais viagens

Também analisei o volume de viagens por mês, separando entre usuários membros e casuais. Usei uma estrutura com `CASE` para transformar o número do mês em nome (janeiro, fevereiro, etc.) para facilitar a leitura. Depois, contei quantas viagens foram feitas em cada mês por cada categoria e ranqueei os meses com maior número de viagens. No entanto, essa análise não mostrou um padrão claro ou diferença significativa entre os dois tipos de usuários.

Código SQL:

```bash
month_count AS (
  SELECT
    member_casual,
	CASE
		WHEN EXTRACT(MONTH FROM start_date) = 1 THEN 'January'
		WHEN EXTRACT(MONTH FROM start_date) = 2 THEN 'February'
		WHEN EXTRACT(MONTH FROM start_date) = 3 THEN 'March'
		WHEN EXTRACT(MONTH FROM start_date) = 4 THEN 'April'
		WHEN EXTRACT(MONTH FROM start_date) = 5 THEN 'May'
		WHEN EXTRACT(MONTH FROM start_date) = 6 THEN 'June'
		WHEN EXTRACT(MONTH FROM start_date) = 7 THEN 'July'
		WHEN EXTRACT(MONTH FROM start_date) = 8 THEN 'August'
		WHEN EXTRACT(MONTH FROM start_date) = 9 THEN 'September'
		WHEN EXTRACT(MONTH FROM start_date) = 10 THEN  'October'
		WHEN EXTRACT(MONTH FROM start_date) = 11 THEN  'November'
		ELSE 'December'
	END AS month_name,
    COUNT(*) AS total
  FROM year_tripdata
  GROUP BY member_casual, month_name
),

month_trips AS(
	SELECT
		member_casual,
		month_name,
		total,
		ROW_NUMBER() OVER(PARTITION BY member_casual ORDER BY total DESC) AS month_rank
	FROM month_count
),

top3_month AS (
SELECT *
FROM month_trips
WHERE month_rank <= 3
)
```

Resultado:

![image.png](img/image%2023.png)

#### Visão geral da análise

Esse código faz um resumo consolidado das análises anteriores, agrupando por tipo de usuário. Ele calcula a média do tempo das viagens e identifica os valores mais comuns para bicicleta usada, estações de início e fim, e o dia da semana com mais viagens. Assim, obtém-se uma visão geral rápida e consolidada do comportamento dos usuários membros e casuais.

Código SQL:

```bash
WITH overview_by_member_type AS (
	SELECT
		member_casual,
		ROUND(AVG(EXTRACT(EPOCH FROM trip_length)/60 ), 2)AS avg_trip_duration,
		MODE() WITHIN GROUP(ORDER BY rideable_type) AS most_comum_bike,
		MODE() WITHIN GROUP(ORDER BY start_station_name) FILTER (WHERE start_station_name != 'empty') AS most_comum_start_station,
		MODE() WITHIN GROUP(ORDER BY end_station_name) FILTER (WHERE end_station_name != 'empty') AS most_comum_end_station,
		MODE() WITHIN GROUP(ORDER BY week_start_day) AS most_comum_start_day
	FROM year_tripdata
	GROUP BY member_casual
),
```

Resultado:

![image.png](img/image%2025.png)

---

### 5. Conclusão

Como os membros anuais e os ciclistas casuais usam as bicicletas Cyclistic de forma diferente?

1. A média de tempo das viagens realizadas por usuários casuais é aproximadamente 71,6% superior à média das viagens dos membros anuais. Isso sugere que os membros anuais realizam viagens próximas a regiões de coleta da bicicleta, enquanto os casuais realizam viagens maiores, provavelmente ao longo da costa do Lago Michigan.
2. A maior parte das viagens realizadas pelos membros anuais (75,8%) concentra-se nos dias úteis, de segunda a sexta-feira, ao passo que os usuários casuais apresentam maior volume de viagens (52,6%) durante o fim de semana, entre sexta e domingo.
3. Proporcionalmente, usuários casuais utilizam _electric_scooters_ cerca de 149,68% mais do que membros anuais, indicando uma forte preferência por esse modelo entre os não assinantes.
4. Analisando um padrão das 5 estações populares para inicio e encerramento de viagens entre categoria, observa-se que os membros anuais utilizam principalmente estações na região central de Chicago, enquanto os usuários casuais iniciam e encerram viagens em estações comumente próximas de áreas de lazer ao longo da costa do Lago Michigan. Isso sugere que os membros, provavelmente residentes ou trabalhadores locais, utilizam o sistema para deslocamentos diários, enquanto os casuais tendem a usar as bicicletas para lazer ou turismo ao redor do lago.

---

### Licença

Projeto: Análise de compartilhamento de bicicletas ciclísticas

Por: Vinicius L. Romão

[LinkedIn](https://www.linkedin.com/in/viniciuslromao/) / [GitHub](https://github.com/viniromao159) / [Kaggle](https://www.kaggle.com/viniciuslromao) / [Tableau](https://public.tableau.com/app/profile/vinicius.lopes.rom.o/vizzes)

## Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT).
