## 📚 Documentation

- [🚀 Quick Start Guide](readme_docs/quickstart_guide.md)
- [🐞 Troubleshooting Tips](readme_docs/troubleshooting_guide.md)
- [⚙️ Project Brief](readme_docs/project_brief.md)
- [🧠 Other Requirements](api/REQUIREMENTS.md)

----------------------------------------

# **Senior Data Engineering Challenge: Real-Time Analytics Platform**

---

### **Executive Summary**

This project implements a prototype for a real-time, multi-tenant analytics platform designed to ingest e-commerce events via Apache Pulsar, process them with Apache Spark, and expose insights via a secure FastAPI layer. Events are streamed, flattened, and batch-loaded into PostgreSQL for querying.

---

### **Architecture Overview**

The architecture consists of a containerized data generator, Pulsar messaging broker, Spark streaming and batch processors, PostgreSQL for storage, and a FastAPI app for exposing an analytics endpoint. The design emphasizes modularity, observability, schema evolution, and developer experience, simulating cloud-native patterns locally.

---

### **Technology Stack Decision**

- **Primary Stack:** Pulsar + Spark
- **Storage Layer:** PostgreSQL and local parquet storage (future Data Lake for parquet storage)
- **API Framework:** FastAPI (async-enabled)
- **Monitoring:** Manual log-monitoring for now (Prometheus+Grafana recommended for future)

**Justification:** Pulsar was chosen for its advanced multi-tenant capabilities and durability. Spark Structured Streaming handles high-throughput processing and schema evolution, while FastAPI provides a modern async API layer. Postgres serves as the initial analytics store with room to grow into data lakes or cloud warehouses.

---

## **System Design Decisions**

---

### **Streaming Architecture**

- **Processing Paradigm:** Lambda-like (real-time for ingestion, batch for analytics)
- **Consistency Model:** At-least-once with idempotency guards (via parquet archive for now)
- **Partitioning Strategy:** Tenant-based topic patterns (e.g., merchant_*.events)
- **State Management:** Stateless Spark micro-batch with durable checkpointing

---

### **Multi-Tenant Architecture**

- **Isolation Level:** Shared infrastructure, logically isolated topics and authorization
- **Data Partitioning:** Row-level, with tenant_id tagging
- **Security Model:** Header-based role with tokens and tenant validation via FastAPI dependencies

---

### **Performance Optimization**

- **Throughput Target:** ~10K events/sec (simulated)
- **Latency Target:** <5s micro-batch delay
- **Scaling Strategy:** Containerized services allow horizontal scaling

---

## **Implementation Highlights**

---

### **Advanced Anomaly Detection**

- *(Not implemented)*
- Mock data includes ML fields like model_scores, enabling future model-based fraud detection

---

### **Real-Time Analytics**

- FastAPI `/metrics` endpoint supports filtering by tenant and timeframe
- SQL queries leverage PostgreSQL JSON operators for flexible querying
- Flattened schema enables future OLAP-style aggregation

---

### **Production Operations**

- **Monitoring Strategy:** Logs and Docker observability
- **Disaster Recovery:** Parquet archive allows reprocessing
- **Security Implementation:** Role-based access with token header and tenant scoping. API design to prevent SQL-injection attacks

---

### **Setup and Deployment**

See these for detailed instructions:

- [🚀 Quick Start Guide](readme_docs/quickstart_guide.md)
- [🐞 Troubleshooting Tips](readme_docs/troubleshooting.md)

---

### **Production Deployment**

- **Future state:** AWS CDK
  - Python-native infrastructure, high level abstractions for things like EMR for spark and EC2 for pulsar

---

### **Performance Benchmarks**

- *Not implemented*

---

### **Throughput Testing**

- Simulated ~100 events/sec in burst mode (needs further testing scaled up)
- Streaming pipeline stabilized under load

---

### **Latency Analysis**

- Stream-to-Postgres latency: ~3–5 seconds in ideal conditions

---

### **Resource Utilization**

- Spark streaming container ~3.5GB RAM at peak
- Batch processor and FastAPI lightweight (<1GB RAM)

---

## **Advanced Features Implemented**

---

### **Schema Evolution**

- JSON payloads include schema_version for future use in logical separation of schema payloads and files
- Pydantic → Spark StructType generation supports future schema upgrades

---

### **Exactly-Once Processing**

- Not fully guaranteed at this time; handled via deduplication potential and file archiving
- Pulsar messages are consumed exactly once

---

### **Multi-Tenant Isolation**

- Topic pattern partitioning (merchant_X.events)
- API security restricts tenant visibility

---

### **Real-Time ML Integration**

- Data pipeline ready for inference — e.g., ml_context already present

---

## **Operational Runbook**

---

### **Monitoring and Alerting**

- Suggested metrics: checkpoint delay, payload ingestion rate, batch success
- Alert on streaming query failure (checkpoint recovery logic)
- Prometheus exporter or Grafana dashboards recommended

---

### **Incident Response**

- If Spark fails: clear checkpoints + parquet
- If Pulsar stalls: restart container + generate new subscription name

---

### **Maintenance Procedures**

- Archive processed parquet files
- Periodic PostgreSQL table vacuuming
- Bump schema version on model changes

---

## **Testing Strategy**

---

### **Unit Testing**

- Flattener logic tested with pytest
- Spark schema inference validated via mocks

---

### **Integration Testing**

- End-to-end: Pulsar → Spark → Postgres → FastAPI validated with real payloads

---

### **Chaos Engineering**

- Simulated container crash + recovery via replay in docker desktop app

---

## **Security and Compliance**

---

### **Data Protection**

- PII simulated + marked via processing_flags (e.g., pii_contains)
- No encryption implemented, but volumes isolated
- Token-based access to API metrics querying

---

### **Compliance Features**

- GDPR, data lineage fields in mock data

---

## **Cost Optimization**

---

### **Resource Efficiency**

- Bind mounts avoid excessive disk use
- Only essential containers run continuously

---

### **Multi-Tenant Cost Allocation**

- Row-level tenant_id supports tracking
- Could expand to resource metering per topic

---

## **Future Enhancements**

Also see docstrings in each module for future enhancement ideas!
---

### **Immediate Improvements**

- Add scheduler for batch job (e.g., cron or Airflow)
- Add additional API endpoints and models

---

### **Medium-Term Roadmap**

- Add a delta lake to store full dataset, adjust data going to PostgreSQL based on needs like aggregations for metrics monitoring
- Add Prometheus monitoring and dashboards

---

### **Long-Term Vision**

- Deploy to cloud
- Use distributed computing via EMR clusters to easily scale up data transformations
- Implement full ML pipeline + feature store integration

---

## **Technical Debt and Limitations**

---

### **Known Limitations**

- No data deduplication
- No retry logic for FastAPI connections

---

### **Technical Debt**

- Column flattening functions need enhancements to flatten array and struct data types more
- Secrets hardcoded in Docker Compose

---

### **Risk Assessment**

- Metadata corruption in Spark can halt stream
- Complex schema can lead to write failures if not sanitized

---

## **Team and Operational Considerations**

---

### **Skill Requirements**

- Python, Docker, PySpark, FastAPI familiarity

---

### **Operational Complexity**

- Moderate: single-node, multiple services with dependencies

---

### **Knowledge Transfer**

- Included: README, API docs, troubleshooting_guide.md, architecture diagram

---

---

**Appendices**

---

**A. Architecture Diagram**

<details>

<summary>📊 Click to expand architecture overview</summary>

```html

+----------------------------+
|  📦 Event Generation       |
|----------------------------|
| - Simulates e-commerce     |
|   events per tenant        |
| - Uses Pydantic data models|
| - Continuous or burst mode |
+----------------------------+
              |
              v
+----------------------------+
|  🔄 Apache Pulsar          |
|----------------------------|
| - Event broker (pub/sub)   |
| - One topic per tenant     |
| - Supports durable streams |
+----------------------------+
              |
              v
+----------------------------+
|  ⚡ Spark Streaming         |
|----------------------------|
| - Real-time processing     |
| - Reads from Pulsar        |
| - Parses & validates JSON  |
| - Flattens to tabular data |
+----------------------------+
              |
              v
+----------------------------+
|  💾 Simulated Data Lake    |
|----------------------------|
| - Local filesystem         |
| - Stores parquet files     |
| - Acts as staging buffer   |
+----------------------------+
             / \
            /   \
           v     v
+----------------------------+      +----------------------------+
|  📥 Spark Batch Processing |      |  ⚡ Spark Streaming         |
|----------------------------|      |  (still running...)         |
| - Runs periodically        |      |                            |
| - Loads parquet into       |      |                            |
|   PostgreSQL via JDBC      |      |                            |
+----------------------------+      +----------------------------+
              |
              v
+----------------------------+
|  🛢️ PostgreSQL              |
|----------------------------|
| - Analytics database       |
| - Stores flattened events  |
+----------------------------+
              |
              v
+----------------------------+
|  🌐 FastAPI Layer           |
|----------------------------|
| - REST API for analytics   |
| - Async DB access          |
| - Uses Pydantic validation |
| - Includes role-based auth |
+----------------------------+

```
</details>



- 🧱 All layers above are Docker containers managed in a docker-compose network.
- Shared volumes allow data movement between Spark and batch services.
- Networked services communicate via container names (pulsar, postgres, etc.)
---

**B. API Documentation**

- Auto-generated with FastAPI at [http://localhost:8000/docs](http://localhost:8000/docs)

---

**C. Configuration Reference**

- **Authorization tokens:**  
  `admin-token`, `tenant1-token`, etc.
- **Mounted volumes:**  
  `spark_output`, `spark_checkpoints`, `postgres_data`

---

**D. Performance Tuning Guide**

- To fill out later

---

**E. Troubleshooting Guide**

- [🐞 Troubleshooting Tips](readme_docs/troubleshooting_guide.md)

---
