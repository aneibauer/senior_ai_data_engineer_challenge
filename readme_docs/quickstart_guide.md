# 🚀 Quick Start Guide

This guide walks you through setting up and running the full system locally from scratch.

⸻

## 🧰 Prerequisites

Before starting, ensure you have the following installed:

	•	Docker Desktop
	•	Docker Compose
	•	Python 3.10+ (for local scripts and development)
	•	Git

## 🧾 1. Clone the Repository

```bash
git@github.com:your_username/senior_ai_data_engineer_challenge.git
cd senior_ai_data_engineer_challenge
```

## 📁 2. Create Required Local Directories

Some Spark services expect local bind-mounted folders. They should be created automatically by docker but just in case:

```bash
mkdir spark_output
mkdir spark_checkpoints
```

## 🐳 3. Start All Services

Run the following command from the root of the project:

```bash
docker compose up --build
```
This will start the following containers:

	•	pulsar: Message broker
	•	postgres: Database with volume persistence
	•	spark: Streaming job to consume Pulsar messages
	•	spark-batch: Batch job that loads parquet files into Postgres
	•	data-generator: Publishes synthetic event data to Pulsar
	•	fastapi: REST API to query metrics from Postgres

Wait until all services show “healthy” or are idle/stable in logs.

## ✅ 4. Verify the FastAPI App

Once the FastAPI container is running, open your browser:
```
http://localhost:8000/docs
```
You should see the Swagger UI with interactive documentation.


⸻

## 🔍 5. Test the API (Curl)

Try querying metrics for a valid tenant (e.g. merchant_1) via curl:

```bash
curl -H "Authorization: admin-token" "http://localhost:8000/api/v2/analytics/realtime/metrics?tenant_id=merchant_1&timeframe=1d"
```

Expected output:
```json
{
  "tenant_id": "merchant_1",
  "event_count": 3, <-will change depending on actual count of events
  "timeframe": "1d"
}
```
If you try querying with an unauthorized token (e.g. tenant1-token for a different tenant), you should receive a 403 Forbidden.

## 🔚 That’s It!

You’ve now:
	•	Bootstrapped the full architecture
	•	Sent test event data via Pulsar
	•	Stored enriched data in Postgres
	•	Queried real-time metrics via FastAPI


## 🛠️ If you need some troublshooting tips, see the troubleshooting_guide