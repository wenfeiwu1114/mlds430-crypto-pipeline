-- stg_crypto_daily.sql
-- Clean the raw Fivetran table

with source as (
    select
        cast(date as date)            as date,
        cast(price as float)          as price,
        cast(market_cap as float)     as market_cap,
        cast(volume as float)         as volume
    from {{ source('coingecko', 'crypto_daily') }}
)

select *
from source