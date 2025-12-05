from fivetran_connector_sdk import Connector, Logging as log, Operations as op
import requests
from datetime import datetime, timezone

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"


def update(configuration: dict, state: dict):
    """
    Fetch Bitcoin market data for the last 365 days
    and send each row to Snowflake using op.upsert().
    """

    log.warning("💰 Starting CoinGecko Connector — Fetching BTC market data")

    params = {
        "vs_currency": "usd",
        "days": "365"
    }

    # --------------------------------------
    # STEP 1: Fetch data
    # --------------------------------------
    try:
        resp = requests.get(COINGECKO_URL, params=params)
        resp.raise_for_status()
        payload = resp.json()
    except Exception as e:
        log.error(f"❌ Error fetching CoinGecko data: {e}")
        return state

    prices = payload.get("prices", [])
    caps = payload.get("market_caps", [])
    volumes = payload.get("total_volumes", [])

    log.warning(f"📦 Retrieved {len(prices)} daily records")

    # --------------------------------------
    # STEP 2: Flatten & UPSERT into Fivetran
    # --------------------------------------
    for i in range(len(prices)):
        ts_ms = prices[i][0]
        price = prices[i][1]
        market_cap = caps[i][1] if i < len(caps) else None
        volume = volumes[i][1] if i < len(volumes) else None

        # Convert timestamp to ISO format
        ts_iso = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat()

        op.upsert(
            table="crypto_daily",
            data={
                "timestamp_utc": ts_iso,
                "date": ts_iso[0:10],
                "price": float(price),
                "market_cap": float(market_cap) if market_cap else None,
                "volume": float(volume) if volume else None
            },
        )

    # --------------------------------------
    # STEP 3: Save checkpoint
    # --------------------------------------
    op.checkpoint(state)
    log.warning("✅ CoinGecko connector run complete — data sent to Fivetran.")

    return state


connector = Connector(update=update)

if __name__ == "__main__":
    connector.debug()