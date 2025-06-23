"""
Senior Data Engineering Challenge: Advanced Event Data Generator

SENIOR-LEVEL REQUIREMENTS:
This is not a simple data generation task. You must architect a production-grade,
multi-tenant event generation system that simulates realistic enterprise patterns.

ADVANCED REQUIREMENTS:
- Generate events matching the complex multi-tenant schema in IMPLEMENTATION_GUIDE.md
- Implement realistic user journey simulation with session correlation
- Create sophisticated fraud patterns for advanced anomaly detection testing
- Support schema evolution and backward compatibility
- Generate correlated cross-tenant patterns while maintaining data isolation
- Implement realistic seasonal trends, geographic clustering, and time-zone effects
- Handle high-throughput generation (10K+ events/second capability)
- Include realistic data quality issues for testing validation frameworks

ARCHITECTURE EXPECTATIONS:
- Multi-threaded/async generation for performance
- Configurable tenant isolation and data distribution
- Realistic business logic simulation (inventory, pricing, promotions)
- Advanced fraud scenario generation (coordinated attacks, account takeovers)
- Memory-efficient handling of large-scale data generation
- Pluggable output destinations (Kafka, Pulsar, files, direct API)

SENIOR EVALUATION CRITERIA:
- Can you design realistic multi-tenant data patterns?
- Do you understand e-commerce business logic complexities?
- Can you simulate sophisticated fraud scenarios?
- Do you implement efficient, scalable generation patterns?
- Can you handle schema evolution and data quality concerns?

This requires deep understanding of distributed systems, e-commerce business logic,
and production data engineering challenges. Simple random data generation will not suffice.
"""

# Your senior-level implementation here
import uuid
import random
import json
from datetime import datetime, timedelta, timezone


# --- Configurable Constants ---
TENANTS = [
    {"tenant_id": "merchant_12345", "merchant_tier": "enterprise", "industry_vertical": "electronics"}, #valid
    {"tenant_id": "merchant_67890", "merchant_tier": "startup", "industry_vertical": "fashion"}, #valid
    {"tenant_id": "merchant_54321", "merchant_tier": "standard", "industry_vertical": "grocery"}, #valid
    {"tenant_id": "merchant_09876", "merchant_tier": "startup", "industry_vertical": "services"}, #valid
    {"tenant_id": "bad_merchant_00001", "merchant_tier": "invalid", "industry_vertical": "unknown"}, #invalid
]

PRODUCTS = [
    {
        "product_id": "sku_789012",
        "category_l1": "Electronics",
        "category_l2": "Smartphones",
        "category_l3": "iPhone",
        "brand": "Apple",
        "model": "iPhone 15 Pro",
        "list_price": 999.99,
        "sale_price": 899.99,
        "currency": "USD"
    }
]
USER_PROFILES = [
    {"account_type": "premium", "verification_status": "verified", "customer_tier": "platinum"},
    {"account_type": "standard", "verification_status": "pending", "customer_tier": "gold"},
]

def random_geo():
    countries = [("US", "New York", "NY", 40.7128, -74.0060), ("DE", "Berlin", "BE", 52.52, 13.405)]
    c = random.choice(countries)
    return {
        "country": c[0],
        "region": c[2],
        "city": c[1],
        "coordinates": {"lat": c[3], "lon": c[4]},
        "accuracy_meters": random.choice([50, 100, 250]),
        "ip_derived": random.choice([True, False])
    }

def random_user_agent():
    browsers = [("Chrome", "120.0.0"), ("Safari", "17.0.1")]
    oses = [("Windows", "11"), ("macOS", "14.0")]
    devices = [("desktop", "Dell"), ("mobile", "Apple")]
    b = random.choice(browsers)
    o = random.choice(oses)
    d = random.choice(devices)
    return {
        "browser": {"name": b[0], "version": b[1]},
        "os": {"name": o[0], "version": o[1]},
        "device": {"type": d[0], "brand": d[1]}
    }

def random_event_type():
    types = [
        ("user_interaction", "page_view"),
        ("transaction", "purchase"),
        ("system_event", "fraud_score"),
        ("ml_inference", "recommendation_click")
    ]
    return random.choice(types)

def random_fraud_score():
    # Simulate rare high-fraud events
    if random.random() < 0.02:
        return round(random.uniform(0.8, 1.0), 2)
    return round(random.uniform(0.01, 0.2), 2)

def random_timestamp(offset_minutes=0):
    now = datetime.now(timezone.utc) + timedelta(minutes=offset_minutes)
    return now.isoformat(timespec='microseconds').replace('+00:00', 'Z')

def generate_event(schema_version="2.1"):
    tenant = random.choice(TENANTS)
    product = random.choice(PRODUCTS)
    user_profile = random.choice(USER_PROFILES)
    event_type, event_subtype = random_event_type()
    fraud_score = random_fraud_score()
    churn_probability = round(random.uniform(0.1, 0.4), 2)

    # Simulate schema evolution: add a new field for v2.2
    extra_field = {}
    if schema_version == "2.2":
        extra_field["new_field_v2_2"] = "example_value"

    event = {
        "schema_version": schema_version,
        "tenant_id": tenant["tenant_id"],
        "partition_key": "user_region_hash",
        "event_metadata": {
            "event_id": str(uuid.uuid4()),
            "correlation_id": str(uuid.uuid4()),
            "causation_id": str(uuid.uuid4()),
            "timestamp": random_timestamp(),
            "ingestion_timestamp": random_timestamp(1),
            "source_system": random.choice(["web_app", "mobile_app", "api", "batch_import"]),
            "event_version": "1.2.3",
            "processing_flags": {
                "requires_enrichment": random.choice([True, False]),
                "pii_contains": random.choice([True, False]),
                "gdpr_subject": random.choice([True, False]),
                "audit_required": random.choice([True, False])
            }
        },
        "event_data": {
            "event_type": event_type,
            "event_subtype": event_subtype,
            "user_context": {
                "user_id": f"user_{random.randint(1000,9999)}",
                "anonymous_id": f"anon_{random.randint(10000,99999)}",
                "session_data": {
                    "session_id": str(uuid.uuid4()),
                    "session_start": random_timestamp(-random.randint(10, 60)),
                    "session_sequence": random.randint(1, 20),
                    "session_attributes": {
                        "device_fingerprint": str(uuid.uuid4())[:16],
                        "geolocation": random_geo(),
                        "user_agent_parsed": random_user_agent()
                    }
                },
                "user_profile": {
                    "account_type": user_profile["account_type"],
                    "registration_date": random_timestamp(-random.randint(1000, 5000)),
                    "verification_status": user_profile["verification_status"],
                    "risk_profile": {
                        "fraud_score": fraud_score,
                        "credit_rating": random.choice(["A", "B", "C", "D"]),
                        "behavioral_flags": random.sample(["high_velocity", "geo_anomaly", "device_change"], k=2)
                    },
                    "preferences": {
                        "communication_channels": random.sample(["email", "sms", "push"], k=2),
                        "privacy_settings": {
                            "tracking_consent": random.choice([True, False]),
                            "marketing_consent": random.choice([True, False]),
                            "analytics_consent": random.choice([True, False])
                        }
                    },
                    "segmentation": {
                        "customer_tier": user_profile["customer_tier"],
                        "lifecycle_stage": random.choice(["acquisition", "activation", "retention", "resurrection"]),
                        "behavioral_segments": random.sample(["high_spender", "mobile_first", "price_sensitive"], k=2),
                        "predictive_scores": {
                            "churn_probability": churn_probability,
                            "lifetime_value": round(random.uniform(500, 2000), 2),
                            "next_purchase_days": random.randint(1, 30)
                        }
                    }
                }
            },
            "business_context": {
                "tenant_metadata": {
                    "merchant_id": tenant["tenant_id"],
                    "merchant_tier": tenant["merchant_tier"],
                    "industry_vertical": tenant["industry_vertical"],
                    "geographic_markets": ["US", "CA", "UK", "DE"],
                    "business_model": random.choice(["b2c", "b2b", "marketplace", "subscription"])
                },
                "transaction_context": {
                    "products": [
                        {
                            "product_id": product["product_id"],
                            "product_hierarchy": {
                                "category_l1": product["category_l1"],
                                "category_l2": product["category_l2"],
                                "category_l3": product["category_l3"],
                                "brand": product["brand"],
                                "model": product["model"]
                            },
                            "pricing": {
                                "list_price": product["list_price"],
                                "sale_price": product["sale_price"],
                                "cost_basis": round(product["sale_price"] * 0.7, 2),
                                "margin_percentage": round((product["sale_price"] - product["sale_price"] * 0.7) / product["sale_price"], 3),
                                "tax_category": random.choice(["standard", "luxury", "exempt"]),
                                "currency": product["currency"]
                            },
                            "inventory": {
                                "sku_availability": random.choice(["in_stock", "low_stock", "backorder", "discontinued"]),
                                "quantity_available": random.randint(0, 100),
                                "warehouse_location": random.choice(["us_east_1", "eu_central_1"]),
                                "supplier_id": f"supplier_{random.randint(100,999)}"
                            },
                            "attributes": {
                                "color": random.choice(["Space Black", "Silver", "Blue"]),
                                "storage": random.choice(["128GB", "256GB", "512GB"]),
                                "condition": random.choice(["new", "refurbished", "used"]),
                                "warranty_months": random.choice([6, 12, 24]),
                                "dimensions": {"height": 159.9, "width": 76.7, "depth": 8.25},
                                "weight_grams": random.randint(200, 250),
                                "certifications": random.sample(["FCC", "CE", "RoHS"], k=2)
                            },
                            "performance_metrics": {
                                "view_count_24h": random.randint(100, 2000),
                                "conversion_rate_7d": round(random.uniform(0.01, 0.1), 3),
                                "return_rate_30d": round(random.uniform(0.01, 0.05), 3),
                                "review_average": round(random.uniform(3.5, 5.0), 1),
                                "review_count": random.randint(100, 2000)
                            }
                        }
                    ],
                    "cart_context": {
                        "cart_id": str(uuid.uuid4()),
                        "cart_value": {
                            "subtotal": round(product["sale_price"] * 2, 2),
                            "tax_breakdown": [
                                {"type": "state_sales_tax", "rate": 0.08, "amount": round(product["sale_price"] * 2 * 0.08, 2)},
                                {"type": "city_tax", "rate": 0.01, "amount": round(product["sale_price"] * 2 * 0.01, 2)}
                            ],
                            "shipping_costs": {
                                "base_shipping": 9.99,
                                "expedited_fee": 15.00,
                                "insurance": 5.99
                            },
                            "discounts_applied": [
                                {
                                    "discount_id": "promo_winter2024",
                                    "discount_type": random.choice(["percentage", "fixed_amount", "buy_x_get_y"]),
                                    "discount_value": 0.10,
                                    "discount_amount": round(product["sale_price"] * 2 * 0.10, 2),
                                    "eligibility_rules": ["min_order_1000", "new_customer"]
                                }
                            ],
                            "loyalty_benefits": {
                                "points_earned": random.randint(50, 200),
                                "points_redeemed": random.randint(0, 100),
                                "tier_bonus_multiplier": round(random.uniform(1.0, 2.0), 1),
                                "cashback_percentage": round(random.uniform(0.01, 0.05), 2)
                            },
                            "final_total": round(product["sale_price"] * 2 * 1.09, 2)
                        },
                        "payment_context": {
                            "payment_methods": [
                                {
                                    "method_type": random.choice(["credit_card", "debit_card", "digital_wallet", "bnpl", "crypto"]),
                                    "provider": random.choice(["visa", "mastercard", "amex", "paypal", "apple_pay", "klarna"]),
                                    "tokenized_identifier": str(uuid.uuid4())[:12],
                                    "billing_address": {
                                        "address_hash": str(uuid.uuid4())[:16],
                                        "country": random.choice(["US", "DE"]),
                                        "postal_code": str(random.randint(10000, 99999)),
                                        "address_type": random.choice(["residential", "commercial", "po_box"])
                                    },
                                    "risk_signals": {
                                        "first_time_payment": random.choice([True, False]),
                                        "velocity_flag": random.choice([True, False]),
                                        "geo_mismatch": random.choice([True, False]),
                                        "fraud_score": fraud_score
                                    }
                                }
                            ],
                            "shipping_context": {
                                "shipping_address": {
                                    "address_hash": str(uuid.uuid4())[:16],
                                    "same_as_billing": random.choice([True, False]),
                                    "country": random.choice(["US", "DE"]),
                                    "postal_code": str(random.randint(10000, 99999)),
                                    "address_type": random.choice(["residential", "commercial", "po_box"])
                                },
                                "shipping_method": {
                                    "carrier": random.choice(["fedex", "ups", "dhl", "usps"]),
                                    "service_level": random.choice(["ground", "express", "overnight", "same_day"]),
                                    "estimated_delivery": random_timestamp(3),
                                    "tracking_enabled": random.choice([True, False]),
                                    "signature_required": random.choice([True, False])
                                }
                            }
                        }
                    }
                },
                "interaction_context": {
                    "touchpoint_journey": [
                        {
                            "touchpoint": random.choice(["google_search", "email_campaign", "social_ad"]),
                            "timestamp": random_timestamp(-random.randint(5, 30)),
                            "attribution_weight": round(random.uniform(0.1, 0.9), 2)
                        }
                    ],
                    "page_context": {
                        "page_type": random.choice(["product_detail", "category", "checkout", "search_results"]),
                        "page_url": "https://example.com/products/iphone-15-pro",
                        "referrer_url": "https://google.com/search?q=iphone+15+pro",
                        "page_load_metrics": {
                            "time_to_first_byte": random.randint(50, 200),
                            "first_contentful_paint": random.randint(500, 1200),
                            "largest_contentful_paint": random.randint(800, 1500),
                            "cumulative_layout_shift": round(random.uniform(0.01, 0.1), 2),
                            "first_input_delay": random.randint(10, 50)
                        },
                        "user_interactions": [
                            {
                                "interaction_type": random.choice(["click", "scroll", "hover", "form_input"]),
                                "element_id": "add_to_cart_button",
                                "timestamp": random_timestamp(),
                                "coordinates": {"x": random.randint(0, 500), "y": random.randint(0, 1000)},
                                "interaction_sequence": random.randint(1, 10)
                            }
                        ]
                    },
                    "experiment_context": {
                        "active_experiments": [
                            {
                                "experiment_id": "checkout_optimization_v3",
                                "variant": random.choice(["treatment_a", "treatment_b"]),
                                "allocation_timestamp": random_timestamp(-random.randint(1, 10)),
                                "experiment_type": random.choice(["ui_test", "algorithm_test", "feature_flag"])
                            }
                        ],
                        "feature_flags": [
                            {
                                "flag_name": "new_recommendation_engine",
                                "enabled": random.choice([True, False]),
                                "variant": "ml_model_v2",
                                "rollout_percentage": random.randint(10, 50)
                            }
                        ]
                    }
                }
            },
            "technical_context": {
                "infrastructure_metadata": {
                    "processing_region": random.choice(["us-east-1", "eu-central-1"]),
                    "availability_zone": random.choice(["us-east-1a", "eu-central-1b"]),
                    "server_instance": f"web-server-{random.randint(1,100):03}",
                    "load_balancer": "alb-prod-web-01",
                    "cdn_edge_location": random.choice(["cloudfront_edge_nyc", "cloudfront_edge_berlin"])
                },
                "performance_telemetry": {
                    "request_id": str(uuid.uuid4()),
                    "trace_id": str(uuid.uuid4()),
                    "parent_span_id": str(uuid.uuid4()),
                    "processing_time_ms": random.randint(10, 100),
                    "memory_usage_mb": random.randint(64, 256),
                    "cpu_utilization": round(random.uniform(0.1, 0.9), 2),
                    "network_latency_ms": random.randint(5, 30),
                    "database_query_time_ms": random.randint(2, 20),
                    "cache_hit_ratio": round(random.uniform(0.7, 0.99), 2)
                },
                "security_context": {
                    "request_signature": str(uuid.uuid4())[:32],
                    "api_key_hash": str(uuid.uuid4())[:32],
                    "rate_limit_remaining": random.randint(9000, 10000),
                    "security_flags": {
                        "suspicious_user_agent": random.choice([False, True, False, False]),
                        "tor_exit_node": random.choice([False, False, True, False]),
                        "known_bot": random.choice([False, False, False, True]),
                        "geo_blocked": random.choice([False, False, False, True])
                    }
                },
                "data_lineage": {
                    "upstream_systems": random.sample(["user_service", "product_catalog", "inventory_service"], k=2),
                    "transformation_applied": random.sample(["pii_tokenization", "geo_enrichment", "fraud_scoring"], k=2),
                    "downstream_targets": random.sample(["data_warehouse", "ml_feature_store", "audit_log"], k=2)
                }
            }
        },
        "ml_context": {
            "feature_vectors": {
                "user_features": [round(random.uniform(0, 1), 2) for _ in range(5)],
                "product_features": [round(random.uniform(0, 1), 2) for _ in range(5)],
                "contextual_features": [round(random.uniform(0, 1), 2) for _ in range(5)]
            },
            "model_scores": {
                "fraud_detection": {
                    "model_version": "fraud_v3.2.1",
                    "score": fraud_score,
                    "confidence": round(random.uniform(0.7, 0.99), 2),
                    "explanation": random.sample(["low_velocity", "known_device", "normal_geo", "ip_blacklist"], k=2)
                },
                "recommendation": {
                    "model_version": "rec_v2.1.0",
                    "recommendations": [
                        {"product_id": "sku_123", "score": round(random.uniform(0.7, 0.99), 2), "reason": "collaborative_filtering"},
                        {"product_id": "sku_456", "score": round(random.uniform(0.6, 0.95), 2), "reason": "content_based"}
                    ]
                },
                "churn_prediction": {
                    "model_version": "churn_v1.5.2",
                    "churn_probability": churn_probability,
                    "days_to_churn": random.randint(10, 90),
                    "intervention_recommended": random.choice(["discount_offer", "personalized_email", "none"])
                }
            }
        }
    }
    event.update(extra_field)
    return event

def generate_events(n=10, schema_version="2.1"):
    for _ in range(n):
        yield generate_event(schema_version=schema_version)

if __name__ == "__main__":
    # Example: generate 3 events, print as JSON lines
    for event in generate_events(3, schema_version="2.1"):
        print(json.dumps(event, indent=2))

