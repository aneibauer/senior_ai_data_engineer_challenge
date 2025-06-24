# 🛠️ Troubleshooting Guide

This guide outlines known issues I ran into during development and step-by-step debugging strategies for running the full event pipeline locally (in docker).

---

## ✅ General Setup Tips

- Create required local directories:

```bash
mkdir -p spark_output spark_checkpoints
```

- Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Make sure Java 17+ is installed (I didn't have it on my machine)
- Use Docker Desktop and ensure it's running

---

## 🐳 Docker Issues

### Restarting from scratch
- Run the following commands:

```bash
docker compose down -v
docker compose up --build
```

- If image changes are not picked up, add `--no-cache`
- Can easily stop and start containers in docker desktop with the play and stop buttons
- Can manually delete containers, images, and volumes from docker desktop

### Container stalls or fails silently?
- Restart Docker Desktop
- Delete all containers/images:

```bash
docker system prune -a
```

---

## 🛰️ Pulsar Debugging

### Check Pulsar health
- Run a health check inside the pulsar container:

```bash
pulsar-admin brokers healthcheck
```

- Can get into bash terminal inside container using command:

```bash
docker exec -it pulsar /bin/bash
```

### Check message flow
- Use pulsar-admin topics stats to check message counters (in and out) for a given topic:

```bash
pulsar-admin topics stats persistent://public/default/merchant_1.events
```

---

## 🔥 Spark Streaming Issues

### Empty DataFrames
- If streaming results are empty, try writing to the console with format console and truncate=false (code update needed temporarily)
- Use a unique subscription name each time the stream is started (implemented already)
- Ensure your data generator container is actually running continuous mode and not burst mode
- Use the following to confirm files are being written:

```bash
docker exec -it spark bash
ls /opt/spark/parquet_output
```

### Batch Metadata Not Found Error
If you see an error like `[BATCH_METADATA_NOT_FOUND]`, try the following:
- Stop everything:

```bash
docker compose down -v
```

- Delete contents of local directories:

```bash
rm -rf spark_output/* spark_checkpoints/*
```

- Rebuild and restart containers:

```bash
docker compose up --build
```

- This could mean the spark data was corrupted somehow

---

## 🐘 Postgres Setup and Debugging

### Postgres CLI Usage
- Enter container:

```bash
docker exec -it postgres /bin/bash
```

- Access database:

```bash
psql -U user -d events
```

- Useful commands:
  - `\dt` lists all tables
  - `\d table_name` shows schema
  - `SELECT * FROM table LIMIT 10;` queries data
  - `\x` toggles expanded mode for large fields

---

## 💥 Table Issues

### Dropping Incorrect Tables
If your table schema is incorrect, run:

```sql
DROP TABLE commerce_events_table;
```

### Column Name Limit
- Postgres limits column names to 63 characters
- If flattening nested fields, names may silently truncate and cause duplication (logic implemented already to shorten the names)

### Data isn't persisted?
You may have accidentally deleted the named volume. The `-v` flag in `docker compose down -v` removes volumes.

---

## ⚡ FastAPI & Security

### Testing API
- Swagger UI available at: http://localhost:8000/docs
- Direct test with curl:

```bash
curl -H "Authorization: admin-token" \
  "http://localhost:8000/api/v2/analytics/realtime/metrics?tenant_id=merchant_7&timeframe=1d"
```

- Currently cannot run GET request via HTTP due to missing authorization piece, so need to run via curl

### Authorization Results
- Valid tenant and token → returns JSON
- Valid token but unauthorized tenant → 403 error
- Invalid token → 401 error

---
