## 📘 README.md — Crypto Analytics Pipeline (Bitcoin Market Dashboard)

Author: Wenfei Wu
Course: MLDS 430 — Data Warehousing & Visualization
Quarter: Fall 2025
Project: End-to-End Cloud Data Pipeline (API → Fivetran → Snowflake → dbt → Tableau)

## 1. Project Overview

This project implements a fully automated, cloud-based analytics pipeline that ingests Bitcoin market data from the CoinGecko API, loads it into Snowflake, transforms it using dbt, and visualizes it in Tableau.

The pipeline showcases modern ELT architecture:

CoinGecko API  
     ↓  
Fivetran Custom Connector  
     ↓  
Snowflake (Raw Layer)  
     ↓  
dbt (Staging → Fact → Dimension Models)  
     ↓  
Tableau Dashboard


The final dashboard provides insights into price trends, market volatility, market cap movement, and daily trading volume.

## 2. Data Source — CoinGecko Bitcoin Market API

Endpoint Used:

https://api.coingecko.com/api/v3/coins/bitcoin/market_chart


Parameters:

vs_currency = usd

days = 365

The API provides arrays of timestamps and values for:

prices

market_caps

total_volumes

Each record corresponds to a historical day.

## 3. Project Structure
project-root/
│── coingecko_connector/        ← Fivetran SDK Connector
│    ├── connector.py
│    ├── requirements.txt
│    └── logs/
│
│── mlds_project/
│    ├── dbt_project.yml
│    ├── profiles.yml   (ignored in Git)
│    └── models/
│         ├── staging/stg_crypto_daily.sql
│         ├── marts/fact_crypto_daily.sql
│         ├── marts/dim_crypto_overview.sql
│         └── schema.yml
│
│── tableau/
│    └── crypto_dashboard.twbx
│
└── README.md

## 4. Flow Pipeline Explanation
1️⃣ API → Fivetran Custom Connector

A Python custom connector (using the Fivetran Connector SDK) makes the API request, parses JSON, and upserts rows into Snowflake.

Connector collects:

Date

Price

Market Cap

Volume

Fivetran manages:

Incremental sync

Schema creation

Scheduling

Change tracking (_fivetran_synced, _fivetran_id)

2️⃣ Fivetran → Snowflake (Raw Table)

Fivetran loads data into:

FIVETRAN_DATABASE.COINGECKO_LYNX.CRYPTO_DAILY


Raw table fields:

date	price	market_cap	volume	_fivetran_synced
3️⃣ Snowflake → dbt Transformations

dbt performs modeling using the Medallion Architecture:

Gold / Fact Layer

fact_crypto_daily

price

market cap

volume

7-day moving averages

analytics-ready structure

Silver / Staging Layer

stg_crypto_daily

type casting

renaming

deduplication

Gold / Dimension Layer

dim_crypto_overview

average price

average market cap

average daily volume

summary statistics for dashboard KPIs

## dbt Models Overview
📌 stg_crypto_daily.sql

Cleans raw crypto data

Standardizes column types

📌 fact_crypto_daily.sql

Adds time-series metrics:

7-day moving average for price

7-day moving average for volume

Used for all line charts.

📌 dim_crypto_overview.sql

Generates summary statistics for the dashboard:

Avg price

Avg market cap

Avg volume

## Tableau Dashboard

The dashboard visualizes:

✔ Bitcoin Price Trend (with 7-day moving average)
✔ Daily Trading Volume Trend
✔ Market Cap Trend
✔ Date Range Filter (interactive)

Uses Snowflake live connection for instant refresh.

## 5. Tableau Visualizations
1. Bitcoin Price Trend

Line chart with moving average

Shows overall price movement and smoothing

2. Daily Volume Trend

Bar/line chart

Highlights trading activity

3. Market Cap Trend

Line chart

Displays macro-level crypto valuation

4. Optional Metrics Visualization

Bar chart comparing:

Average Price

Average Market Cap

Average Volume

Dashboard Filters

User-adjustable date range

Affects all plots simultaneously

## 6. Technologies Used
Category	Tool
API Source	CoinGecko Bitcoin Market API
Ingestion	Fivetran Custom Connector SDK
Storage	Snowflake Data Warehouse
Transformation	dbt Core
Visualization	Tableau Desktop
Language	Python (3.9)
## 7. How to Reproduce This Project
Clone or download this repo
git clone https://github.com/your_repo/mlds430-crypto-pipeline.git

Install Fivetran Connector SDK
pip install fivetran-connector-sdk

Deploy Connector
fivetran deploy --api-key <KEY> --destination Warehouse --connection coingecko_lynx

Run dbt models
cd mlds_project
dbt run
dbt test

Open Tableau Dashboard

Connect to Snowflake:

Database → FIVETRAN_DATABASE

Schema → COINGECKO_LYNX

Tables → FACT_CRYPTO_DAILY, DIM_CRYPTO_OVERVIEW

## 8. Project Screenshots

Add screenshots of:

Fivetran connection

Snowflake raw table

dbt models

Tableau dashboard

(Use your own screenshots here)

## 9. Learnings & Takeaways

How to build automated API ingestion using Fivetran

Best practices for Snowflake schema + roles

Importance of dbt staging + fact model separation

Moving average calculations for time-series analysis

Tableau dashboard design for financial datasets

Full cloud ELT architecture experience

## 10. Future Improvements

Add correlation analysis between volume and price

Include multiple cryptocurrencies

Build volatility indicators (returns, standard deviation)

Automate dbt with Airflow (extra credit)

Add anomaly detection using Python