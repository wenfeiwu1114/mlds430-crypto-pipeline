-- fact_crypto_daily.sql
-- Create metrics for dashboard use

with base as (
    select *
    from {{ ref('stg_crypto_daily') }}
),

metrics as (
    select
        date,
        price,
        market_cap,
        volume,
        avg(price) over (order by date rows between 6 preceding and current row) as price_7day_avg,
        avg(volume) over (order by date rows between 6 preceding and current row) as volume_7day_avg
    from base
)

select *
from metrics