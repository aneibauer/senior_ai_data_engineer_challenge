## 🧠 What is Apache Pulsar and Why Are We Using It?

Apache Pulsar is a high-performance, distributed message broker. In this system, Pulsar acts as the **real-time event streaming layer** that connects simulated client/vendor events to downstream processing systems like Spark.

### 🔁 Pulsar Is Not a Database

Pulsar does **not** store data permanently. Instead, it:

- **Ingests** event streams from multiple producers (e.g., tenants/vendors)
- **Buffers** those events temporarily with strong delivery guarantees
- **Distributes** the events to one or more consumers (e.g., Spark jobs, APIs)

Messages are stored internally via BookKeeper and can be retained temporarily based on subscription behavior or retention policies.

---

## 🔗 Where Pulsar Fits in This Architecture
Vendors / Data Generator
⬇
Pulsar  ← 🧠 Message broker (per-tenant topics)
⬇
Spark  ← Event consumer (validation, enrichment, ML)
⬇
Delta Lake / Postgres ← Long-term storage and APIs

---

## ✅ Why Use Pulsar?

| Benefit          | Description |
|------------------|-------------|
| **Multi-tenancy** | Events can be published to tenant-specific topics (e.g., `merchant_12345.events`) |
| **Scalability**  | Pulsar can handle hundreds of thousands of events per second |
| **Decoupling**   | Producers and consumers operate independently without knowing each other's state |
| **Replayability**| Consumers can replay messages based on subscription settings |
| **Streaming Ready** | Ideal for structured streaming pipelines like PySpark |

---

## 🧩 Is Pulsar a Storage Layer?

No. Pulsar stores messages **temporarily**, either:

- Until acknowledged (based on subscription type)
- For a limited time, based on **retention policies**

If you want **permanent storage**, connect Pulsar to systems like:

- Delta Lake (for historical data & analytics)
- PostgreSQL (for queryable alerts or summaries)
- Object stores (e.g., S3)

---

## 🔥 Summary

Pulsar is the **event backbone** of this system. It enables:

- Vendor-agnostic message ingestion
- Tenant-specific routing and isolation
- Stream-oriented processing pipelines
- Scalable, fault-tolerant decoupling of producers and consumers

It’s the glue between **real-time events** and **durable analytics**.