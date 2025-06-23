from pydantic import BaseModel, Field, AfterValidator, BeforeValidator
from typing import List, Optional, Annotated, Literal
from datetime import datetime, timedelta
import pycountry
from enum import Enum



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