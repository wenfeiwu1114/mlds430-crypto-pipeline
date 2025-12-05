select
    min(date) as start_date,
    max(date) as end_date,
    avg(price) as avg_price,
    avg(volume) as avg_volume,
    avg(market_cap) as avg_market_cap
from {{ ref('stg_crypto_daily') }}