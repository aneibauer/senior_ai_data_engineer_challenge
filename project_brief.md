# Senior Data Engineering Challenge: Real-Time Analytics Platform

## Overview
Design and implement a **production-grade, distributed data processing platform** that handles multi-tenant e-commerce events at scale. **Time Limit: 2 hours**

## Senior-Level Expectations
This challenge assumes you have **5+ years of production data engineering experience** and deep expertise in:
- Distributed streaming architectures
- Complex event processing and schema evolution
- Advanced anomaly detection algorithms
- Multi-tenant data isolation and security
- Production monitoring and observability
- Performance optimization under load

## Business Context
You're the **Senior Data Engineer** tasked with building the core data platform for a **multi-billion dollar e-commerce company** that processes:
- **100M+ events/day** across 10,000+ merchants
- **Real-time fraud detection** with <50ms latency requirements
- **Multi-region deployment** with cross-region replication
- **GDPR/SOX compliance** with audit trails
- **99.99% uptime SLA** with automatic failover

## Architecture Requirements

### Non-Negotiable Requirements
- **Exactly-once processing** guarantees
- **Schema evolution** support without downtime
- **Multi-tenant data isolation** with security boundaries
- **Horizontal scalability** to 10x current load
- **Disaster recovery** with <1 hour RTO
- **Real-time alerting** on data quality issues
- **Cost optimization** strategies

## Challenge Phases

### Phase 1: Advanced Architecture Design (30 minutes)
- **Distributed streaming architecture** with fault tolerance
- **Schema registry** with backward compatibility
- **Multi-tenant data partitioning** strategy
- **Security and compliance** framework

### Phase 2: Complex Event Processing (60 minutes)
- **Advanced anomaly detection** with ML integration
- **Complex event correlation** across sessions and users
- **Real-time feature engineering** for downstream ML
- **Performance optimization** for high-throughput processing

### Phase 3: Production Operations (30 minutes)
- **Monitoring and alerting** with custom metrics
- **Auto-scaling and load balancing**
- **Data quality validation** framework
- **Operational runbooks** and incident response

## Technical Leadership Expectations
As a senior engineer, you must demonstrate:
- **System design thinking** - Why did you choose this architecture?
- **Trade-off analysis** - What are the costs and benefits?
- **Operational excellence** - How do you ensure reliability?
- **Performance engineering** - How do you optimize for scale?
- **Security mindset** - How do you protect sensitive data?

## Evaluation Criteria
- **Architecture Quality** (30%) - Distributed design, scalability, fault tolerance
- **Implementation Excellence** (25%) - Code quality, performance, security
- **Operational Readiness** (25%) - Monitoring, alerting, disaster recovery
- **Senior-Level Judgment** (20%) - Decision justification, trade-off analysis

## Success Metrics
Your solution must demonstrate:
- **Processing 10K+ events/second** with <100ms latency
- **Detection of complex fraud patterns** across multiple data points
- **Zero data loss** during simulated failures
- **Sub-second response times** for analytics queries
- **Production-ready code** with proper error handling

