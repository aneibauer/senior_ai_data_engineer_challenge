# Senior Data Engineering Challenge: Advanced Real-Time Stream Processor

## SENIOR-LEVEL REQUIREMENTS

Design and implement a production-grade, distributed stream processing system capable of handling enterprise-scale e-commerce event streams with strict SLA requirements and multi-tenant isolation.

## ADVANCED ARCHITECTURE EXPECTATIONS

- Process 10K+ events/second with <50ms end-to-end latency
- Implement exactly-once processing semantics with idempotency guarantees
- Design multi-tenant data isolation with performance optimization
- Handle schema evolution without downtime (backward/forward compatibility)
- Implement sophisticated state management with fault tolerance
- Build complex event correlation across sessions, users, and time windows
- Design real-time feature engineering pipeline for ML model serving

## COMPLEX EVENT PROCESSING REQUIREMENTS

- Advanced windowing strategies (tumbling, sliding, session-based)
- Cross-stream joins with temporal constraints
- Complex aggregations with custom business logic
- Event-time vs processing-time handling with watermarking
- Late-arriving data handling with configurable tolerance
- Real-time model scoring integration with sub-millisecond latency

## PRODUCTION OPERATIONAL REQUIREMENTS

- Comprehensive error handling with circuit breakers
- Backpressure management and load shedding
- Distributed tracing and structured logging
- Custom metrics emission for business and technical monitoring
- Graceful shutdown and startup procedures
- Memory management for high-throughput processing

## SENIOR EVALUATION CRITERIA

- Can you architect distributed streaming systems at scale?
- Do you understand streaming semantics and trade-offs?
- Can you implement complex business logic in streaming context?
- Do you design for operational excellence and observability?
- Can you optimize for both performance and resource efficiency?
- Do you handle edge cases and failure scenarios properly?

## TECHNOLOGY STACK DECISION

Choose and justify one of: Kafka+Flink, Pulsar+Spark, or Cloud-Native Beam

Your choice will be evaluated based on requirements fit and trade-off analysis.

---

*This is a senior-level distributed systems challenge requiring deep expertise in stream processing, event-driven architectures, and production operations.*
