from pydantic import BaseModel, Field, AfterValidator, BeforeValidator
from typing import List, Optional, Annotated, Literal
from datetime import datetime, timedelta
from faker import Faker
import random
import uuid

from data_generator.models.user import (
    CountryCodeEnum,
    BrowserEnum,
    OSNameEnum,
    DeviceTypeEnum,
    DeviceBrandEnum,
    LifecycleStageEnum,
    AccountTypeEnum,
    Coordinates,
    GeoLocation,
    BrowserInfo,
    OSInfo,
    DeviceInfo,
    UserAgentParsed,
    SessionAttributes,
    SessionData,
    RiskProfile,
    Preferences,
    PrivacySettings,
    PredictiveScores,
    Segmentation,
    UserProfile,
    UserContext
)

fake = Faker()

def make_geo_location() -> GeoLocation:
    return GeoLocation(
        country=random.choice(list(CountryCodeEnum)),
        region="California", #randomize later
        city="Los Angeles", #randomize later
        coordinates=Coordinates(lat=random.uniform(-90.0,90.0), lon=random.uniform(-180.0,180.0)),
        accuracy_meters=random.randint(100, 10000),  # Random accuracy in meters
        ip_derived=random.choice([True, False])
    )

def make_user_agent() -> UserAgentParsed:
    return UserAgentParsed(
        browser=BrowserInfo(name=random.choice(list(BrowserEnum)), version="120.0.0"),
        os=OSInfo(name=random.choice(list(OSNameEnum)), version="11"),
        device=DeviceInfo(type=random.choice(list(DeviceTypeEnum)), brand=random.choice(list(DeviceBrandEnum)))
    )

def make_session_data() -> SessionData:
    now = datetime.now()
    return SessionData(
        session_id=str(uuid.uuid4()),
        session_start=now - timedelta(minutes=random.randint(1, 30)),
        session_sequence=random.randint(1, 50), #future: make another session with next session sequence id
        session_attributes=SessionAttributes(
            device_fingerprint=fake.sha256(),
            geolocation=make_geo_location(),
            user_agent_parsed=make_user_agent()
        )
    )


def make_user_profile() -> UserProfile:
    return UserProfile(
        account_type=random.choice(list(AccountTypeEnum)),
        registration_date=datetime(random.randint(2020,2025), random.randint(1,12), random.randint(1,31)),
        verification_status=random.choice(["verified", "pending", "unverified"]),
        
        risk_profile=RiskProfile(
            fraud_score=round(random.uniform(0.0, 1.0), 2),
            credit_rating=random.choice(["A", "B", "C", "D","F"]),
            behavioral_flags=random.sample(["high_velocity", "geo_anomaly", "none"], 2)
        ),
       
        preferences=Preferences(
            communication_channels=random.sample(["email", "sms", "push"], 2),
            privacy_settings=PrivacySettings(
                tracking_consent=random.choice([True, False]),
                marketing_consent=random.choice([True, False]),
                analytics_consent=random.choice([True, False])
            )
        ),

        segmentation=Segmentation(
            customer_tier=random.choice(["platinum", "gold", "silver", "bronze"]),
            lifecycle_stage=random.choice(list(LifecycleStageEnum)),
            behavioral_segments=random.sample(["high_spender", "mobile_first", "price_sensitive"], 2),
            predictive_scores=PredictiveScores(
                churn_probability=round(random.uniform(0.0, 1.0), 2),
                lifetime_value=round(random.uniform(100, 5000), 2),
                next_purchase_days=random.randint(1, 60)
            )
        )
    )

def make_user_context() -> UserContext:
    return UserContext(
        user_id=fake.sha256(),
        anonymous_id=str(uuid.uuid4()),
        session_data=make_session_data(),
        user_profile=make_user_profile()
    )

#tested and working
# if __name__ == "__main__":
#     user_context = make_user_context()
#     print(user_context.model_dump_json(indent=2))  # Print the user context in a readable JSON form
