from pydantic import BaseModel, Field, AfterValidator, BeforeValidator
from typing import List, Optional, Annotated, Literal
from datetime import datetime, timedelta
import pycountry
from enum import Enum
from faker import Faker
import random
import uuid

fake = Faker()


country_codes = [country.alpha_2 for country in pycountry.countries]
country_enum_data = {code: code for code in country_codes}
CountryCodeEnum = Enum('CountryCodeEnum', country_enum_data)

class BrowserEnum(Enum):
    CHROME = "Chrome"
    FIREFOX = "Firefox"
    SAFARI = "Safari"
    EDGE = "Edge"
    OPERA = "Opera"
    INTERNET_EXPLORER = "Internet Explorer"

class OSNameEnum(Enum):
    WINDOWS = "Windows"
    MACOS = "macOS"
    LINUX = "Linux"
    ANDROID = "Android"
    IOS = "iOS"
    OTHER = "Other"

class DeviceTypeEnum(Enum):
    DESKTOP = "Desktop"
    MOBILE = "Mobile"
    TABLET = "Tablet"
    SMART_TV = "Smart TV"
    WEARABLE = "Wearable"
    OTHER = "Other"

class DeviceBrandEnum(Enum):
    APPLE = "Apple"
    SAMSUNG = "Samsung"
    GOOGLE = "Google"
    HUAWEI = "Huawei"
    XIAOMI = "Xiaomi"
    SONY = "Sony"
    LG = "LG"
    DELL = "Dell"
    OTHER = "Other"

class LifecycleStageEnum(Enum):
    ACQUISITION = "Acquisition"
    ACTIVATION = "Activation"
    RETENTION = "Retention"
    RESURRECTION = "Resurrection"
 
class AccountTypeEnum(Enum):
    PREMIUM = "Premium"
    STANDARD = "Standard"
    TRIAL = "Trial"
    ENTERPRISE = "Enterprise"

class Coordinates(BaseModel):
    lat: float = Field(gt=-90, le=90, description="Latitude in degrees, between -90 and 90")
    lon: float = Field(gt=-180, le=180, description="Longitude in degrees, between -180 and 180")


class GeoLocation(BaseModel):
    country: CountryCodeEnum
    region: str
    city: str
    coordinates: Coordinates
    accuracy_meters: int
    ip_derived: bool


class BrowserInfo(BaseModel):
    name: BrowserEnum
    version: str


class OSInfo(BaseModel):
    name: OSNameEnum
    version: str


class DeviceInfo(BaseModel):
    type: DeviceTypeEnum
    brand: DeviceBrandEnum


class UserAgentParsed(BaseModel):
    browser: BrowserInfo
    os: OSInfo
    device: DeviceInfo


class SessionAttributes(BaseModel):
    device_fingerprint: str
    geolocation: GeoLocation
    user_agent_parsed: UserAgentParsed


class SessionData(BaseModel):
    session_id: str
    session_start: datetime
    session_sequence: int
    session_attributes: SessionAttributes


class RiskProfile(BaseModel):
    fraud_score: float
    credit_rating: Literal['A', 'B', 'C', 'D', 'F']
    behavioral_flags: List[str]


class PrivacySettings(BaseModel):
    tracking_consent: bool
    marketing_consent: bool
    analytics_consent: bool


class Preferences(BaseModel):
    communication_channels: List[str]
    privacy_settings: PrivacySettings


class PredictiveScores(BaseModel):
    churn_probability: float = Field(gt=0, le=1, description="Churn probability between 0 and 1")
    lifetime_value: float
    next_purchase_days: int


class Segmentation(BaseModel):
    customer_tier: str
    lifecycle_stage: LifecycleStageEnum
    behavioral_segments: List[str]
    predictive_scores: PredictiveScores


class UserProfile(BaseModel):
    account_type: AccountTypeEnum
    registration_date: datetime
    verification_status: Literal['verified', 'pending', 'unverified']
    risk_profile: RiskProfile
    preferences: Preferences
    segmentation: Segmentation


class UserContext(BaseModel):
    user_id: str
    anonymous_id: str
    session_data: SessionData
    user_profile: UserProfile


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
if __name__ == "__main__":
    user_context = make_user_context()
    print(user_context.model_dump_json(indent=2))  # Print the user context in a readable JSON form
