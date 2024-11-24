-- First create the table
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,  -- YYYYMMDD format
    date_actual DATE NOT NULL,
    day_of_week INT NOT NULL,  -- 1 to 7
    day_name VARCHAR(10) NOT NULL,  -- Monday, Tuesday, etc.
    day_of_month INT NOT NULL,  -- 1 to 31
    day_of_year INT NOT NULL,  -- 1 to 366
    week_of_year INT NOT NULL,  -- 1 to 53
    month_actual INT NOT NULL,  -- 1 to 12
    month_name VARCHAR(10) NOT NULL,  -- January, February, etc.
    quarter_actual INT NOT NULL,  -- 1 to 4
    year_actual INT NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN NOT NULL DEFAULT FALSE
);

-- Then populate it with a series of dates
-- This example uses PostgreSQL-specific syntax
INSERT INTO dim_date
SELECT
    TO_CHAR(datum, 'YYYYMMDD')::INT AS date_key,
    datum AS date_actual,
    EXTRACT(DOW FROM datum) + 1 AS day_of_week,
    TO_CHAR(datum, 'Day') AS day_name,
    EXTRACT(DAY FROM datum) AS day_of_month,
    EXTRACT(DOY FROM datum) AS day_of_year,
    EXTRACT(WEEK FROM datum) AS week_of_year,
    EXTRACT(MONTH FROM datum) AS month_actual,
    TO_CHAR(datum, 'Month') AS month_name,
    EXTRACT(QUARTER FROM datum) AS quarter_actual,
    EXTRACT(YEAR FROM datum) AS year_actual,
    CASE
        WHEN EXTRACT(DOW FROM datum) IN (6, 0) THEN TRUE
        ELSE FALSE
    END AS is_weekend,
    FALSE AS is_holiday
FROM (
    -- Generate dates for 10 years
    SELECT '2020-01-01'::DATE + SEQUENCE.DAY AS datum
    FROM GENERATE_SERIES(0, 3650) AS SEQUENCE(DAY)
) DQ
ORDER BY 1;