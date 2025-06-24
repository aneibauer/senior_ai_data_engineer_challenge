from pydantic import BaseModel, BeforeValidator, Field
from typing import List, Optional, Annotated, Literal
from datetime import datetime
import uuid
from enum import Enum
import random
from data_generator.models.user import CountryCodeEnum
from datetime import datetime, timedelta

class Verticals(Enum):
    ELECTRONICS = "electronics"
    FASHION = "fashion"
    GROCERY = "grocery"
    SERVICES = "services"

CATEGORY_TREE = {
    "electronics": {
        "Smartphones": ["iPhone", "Samsung Galaxy", "Pixel"],
        "Laptops": ["MacBook Pro", "Dell XPS", "Lenovo ThinkPad"],
        "TVs": ["OLED", "QLED", "4K Smart TV"],
        "Brands": ["Apple", "Samsung", "Sony", "LG", "Dell"]
    },
    "fashion": {
        "Men's Clothing": ["Suits", "Jeans", "Shirts"],
        "Women's Clothing": ["Dresses", "Handbags", "Blouses"],
        "Shoes": ["Sneakers", "Boots", "Heels"],
        "Brands": ["Nike", "Adidas", "Zara", "H&M", "Gucci"]
    },
    "services": {
        "Financial": ["Tax Prep", "Insurance", "Loans"],
        "Health & Wellness": ["Therapy", "Yoga", "Nutrition"],
        "Home Services": ["Plumbing", "Cleaning", "Electrician"],
        "Brands": ["ServiceMaster", "Angie's List", "TaskRabbit"]
    },
    "grocery": {
        "Produce": ["Fruits", "Vegetables", "Organic"],
        "Beverages": ["Juice", "Soda", "Coffee"],
        "Packaged Goods": ["Cereal", "Snacks", "Canned Food"],
        "Brands": ["Whole Foods", "Trader Joe's", "Kroger", "Walmart"]
    }
}

class CurrencyEnum(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    AUD = "AUD"

class AvailabilityStatus(Enum):
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    DISCONTINUED = "discontinued"
    BACKORDER = "backorder"

class ColorEnum(Enum):
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    BLACK = "Black"
    WHITE = "White"
    YELLOW = "Yellow"
    ORANGE = "Orange"
    PURPLE = "Purple"
    PINK = "Pink"


# --- Product Hierarchy & Pricing ---

class ProductHierarchy(BaseModel):
    category_l1: Verticals
    category_l2: str
    category_l3: str
    brand: str
    model: str


class Pricing(BaseModel):
    list_price: float
    sale_price: float
    cost_basis: float
    margin_percentage: float
    tax_category: Literal['standard','luxury','exempt']
    currency: CurrencyEnum


# --- Inventory & Product Attributes ---

class Inventory(BaseModel):
    sku_availability: AvailabilityStatus
    quantity_available: int
    warehouse_location: str
    supplier_id: str


class Dimensions(BaseModel):
    height: float
    width: float
    depth: float


class ProductAttributes(BaseModel):
    color: ColorEnum
    storage: str
    condition: Literal['new', 'refurbished', 'used']
    warranty_months: int
    dimensions: Dimensions
    weight_grams: int
    certifications: List[str]


# --- Performance Metrics ---

class PerformanceMetrics(BaseModel):
    view_count_24h: int
    conversion_rate_7d: float
    return_rate_30d: float
    review_average: float
    review_count: int


# --- Full Product Object ---

class Product(BaseModel):
    product_id: str
    product_hierarchy: ProductHierarchy
    pricing: Pricing
    inventory: Inventory
    attributes: ProductAttributes
    performance_metrics: PerformanceMetrics


# --- Cart Value Breakdown ---

class TaxBreakdown(BaseModel):
    type: Literal['state_sales_tax', 'city_tax', 'federal_tax', 'luxury_tax']
    rate: float = Field(gt=0, le=0.2, description="Tax rate between 0 and .2")
    amount: float


class ShippingCosts(BaseModel):
    base_shipping: float
    expedited_fee: float
    insurance: float


class Discount(BaseModel):
    discount_id: str
    discount_type: Literal['percentage', 'fixed_amount', 'buy_x_get_y']
    discount_value: float
    discount_amount: float
    eligibility_rules: List[str]


class LoyaltyBenefits(BaseModel):
    points_earned: int
    points_redeemed: int
    tier_bonus_multiplier: float
    cashback_percentage: float


class CartValue(BaseModel):
    subtotal: float
    tax_breakdown: List[TaxBreakdown]
    shipping_costs: ShippingCosts
    discounts_applied: List[Discount]
    loyalty_benefits: LoyaltyBenefits
    final_total: float


# --- Payment Context ---

class BillingAddress(BaseModel):
    address_hash: str
    country: CountryCodeEnum
    postal_code: str
    address_type: Literal['residential', 'commercial', 'po_box']


class RiskSignals(BaseModel):
    first_time_payment: bool
    velocity_flag: bool
    geo_mismatch: bool
    fraud_score: float = Field(gt=0, le=1, description="Fraud score between 0 and 1")

class PaymentMethodType(Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    DIGITAL_WALLET = "digital_wallet"
    BNPL = "bnpl"  # Buy Now Pay Later
    CRYPTO = "crypto"

class ProviderEnum(Enum):
    VISA = "Visa"
    MASTERCARD = "MasterCard"
    AMEX = "American Express"
    PAYPAL = "PayPal"
    KLARNA = "Klarna"
    APPLE_PAY = "Apple Pay"
    GOOGLE_PAY = "Google Pay"
    CRYPTOCURRENCY = "Cryptocurrency"  # Generic for crypto payments
    
class PaymentMethod(BaseModel):
    method_type: PaymentMethodType
    provider: ProviderEnum
    tokenized_identifier: str
    billing_address: BillingAddress
    risk_signals: RiskSignals


class ShippingAddress(BaseModel):
    address_hash: str
    same_as_billing: bool
    country: CountryCodeEnum
    postal_code: str
    address_type: Literal['residential', 'commercial', 'po_box']


class ShippingMethod(BaseModel):
    carrier: Literal['fedex', 'ups', 'usps', 'dhl']
    service_level: Literal['ground','express','overnight', 'same_day']
    estimated_delivery: datetime
    tracking_enabled: bool
    signature_required: bool


class ShippingContext(BaseModel):
    shipping_address: ShippingAddress
    shipping_method: ShippingMethod


class PaymentContext(BaseModel):
    payment_methods: List[PaymentMethod]
    shipping_context: ShippingContext


# --- Cart & Transaction Context ---

class CartContext(BaseModel):
    cart_id: str
    cart_value: CartValue
    payment_context: PaymentContext


class TransactionContext(BaseModel):
    products: List[Product]
    cart_context: CartContext


# --- Merchant Metadata ---

class TenantMetadata(BaseModel):
    merchant_id: str
    merchant_tier: Literal['enterprise', 'standard', 'startup']
    industry_vertical: Verticals
    geographic_markets: List[CountryCodeEnum]
    business_model: Literal['b2c', 'b2b', 'marketplace', 'subscription']


# --- Full Business Context ---

class BusinessContext(BaseModel):
    tenant_metadata: TenantMetadata
    transaction_context: TransactionContext
    # interaction_context is in a separate module
