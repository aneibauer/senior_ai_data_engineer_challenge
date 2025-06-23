from pydantic import BaseModel, BeforeValidator, Field
from typing import List, Optional, Annotated, Literal
from datetime import datetime
import uuid
from enum import Enum
import random
from .user import CountryCodeEnum
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


# def generate_product_category(vertical: Verticals) -> tuple[str, str, str]:
#     l2_categories = CATEGORY_TREE[vertical.value]
#     category_l2 = random.choice([k for k in l2_categories.keys() if k != "Brands"])
#     category_l3 = random.choice(l2_categories[category_l2])
#     brand = random.choice(l2_categories["Brands"])
#     return category_l2, category_l3, brand


# --- Product Hierarchy & Pricing ---

class ProductHierarchy(BaseModel):
    category_l1: Annotated[Verticals, BeforeValidator(lambda v: v.lower())]
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
    # interaction_context will go in a separate module


# Business Data Factory Functions

def make_product_hierarchy() -> ProductHierarchy:
    vertical = random.choice(list(Verticals))
    category_tree = CATEGORY_TREE[vertical.value]
    category_l2 = random.choice([k for k in category_tree if k != "Brands"])
    category_l3 = random.choice(category_tree[category_l2])
    brand = random.choice(category_tree["Brands"])

    return ProductHierarchy(
        category_l1=vertical,
        category_l2=category_l2,
        category_l3=category_l3,
        brand=brand,
        model=f"{brand} {category_l3}"
    )


def make_pricing() -> Pricing:
    list_price = round(random.uniform(10, 2000), 2)
    sale_discount = random.uniform(0.05, 0.25)
    sale_price = round(list_price * (1 - sale_discount), 2)
    cost_basis = round(list_price * random.uniform(0.4, 0.7), 2)
    margin = round((sale_price - cost_basis) / sale_price, 3)
    tax_category = random.choice(["standard", "luxury", "exempt"])
    currency = random.choice(list(CurrencyEnum))

    return Pricing(
        list_price=list_price,
        sale_price=sale_price,
        cost_basis=cost_basis,
        margin_percentage=margin,
        tax_category=tax_category,
        currency=currency
    )

def make_inventory() -> Inventory:
    return Inventory(
        sku_availability=random.choice(list(AvailabilityStatus)),
        quantity_available=random.randint(0, 150),
        warehouse_location=random.choice(["us_east_1", "us_west_2", "eu_central_1"]),
        supplier_id=f"supplier_{random.randint(100, 999)}"
    )


def make_product_attributes() -> ProductAttributes:
    return ProductAttributes(
        color=random.choice(list(ColorEnum)),
        storage=random.choice(["64GB", "128GB", "256GB", "512GB", "1TB"]),
        condition=random.choice(["new", "refurbished", "used"]),
        warranty_months=random.choice([6, 12, 24, 36]),
        dimensions=Dimensions(
            height=round(random.uniform(10.0, 200.0), 2),
            width=round(random.uniform(10.0, 100.0), 2),
            depth=round(random.uniform(1.0, 20.0), 2)
        ),
        weight_grams=random.randint(100, 3000),
        certifications=random.sample(["FCC", "CE", "RoHS", "UL", "EnergyStar"], k=random.randint(1, 3))
    )

def make_performance_metrics() -> PerformanceMetrics:
    return PerformanceMetrics(
        view_count_24h=random.randint(0, 5000),
        conversion_rate_7d=round(random.uniform(0.005, 0.15), 4),
        return_rate_30d=round(random.uniform(0.0, 0.25), 4),
        review_average=round(random.uniform(1.0, 5.0), 2),
        review_count=random.randint(0, 5000)
    )

def make_product() -> Product:
    return Product(
        product_id=f"sku_{uuid.uuid4().hex[:8]}",
        product_hierarchy=make_product_hierarchy(),
        pricing=make_pricing(),
        inventory=make_inventory(),
        attributes=make_product_attributes(),
        performance_metrics=make_performance_metrics()
    )


def make_products() -> List[Product]:
    return [make_product() for _ in range(random.randint(1, 3))]


def make_tax_breakdown(subtotal: float) -> List[TaxBreakdown]:
    tax_types = ['state_sales_tax', 'city_tax', 'federal_tax', 'luxury_tax']
    selected_types = random.sample(tax_types, k=random.randint(1, min(3, len(tax_types))))
    rates=[round(random.uniform(0.01, 0.2), 3) for _ in selected_types]
    types_and_rates = zip(selected_types, rates)
    
    return [
        TaxBreakdown(
            type = tax_type,
            rate = rate,
            amount=round(subtotal * rate, 2)
        )
        for tax_type,rate in types_and_rates
    ]


def make_shipping_costs() -> ShippingCosts:
    return ShippingCosts(
        base_shipping=round(random.uniform(5.0, 15.0), 2),
        expedited_fee=round(random.uniform(10.0, 25.0), 2),
        insurance=round(random.uniform(2.0, 7.0), 2)
    )

class DiscountOptions(Enum):
    PROMO_WINTER = "promo_winter"
    PROMO_SUMMER = "promo_summer"
    PROMO_BACK_TO_SCHOOL = "promo_back_to_school"
    PROMO_BLACK_FRIDAY = "promo_black_friday"

def make_discounts(subtotal: float) -> List[Discount]:
    discount_value = random.uniform(0.05, 0.50)  # Discount between 5% and 50%
    discount_amount = round(subtotal * discount_value, 2)
    return [
        Discount(
            discount_id=f"{random.choice(list(DiscountOptions)).value}_{random.randint(2020, 2025)}",
            discount_type="percentage",
            discount_value=discount_value,
            discount_amount=discount_amount,
            eligibility_rules=["min_order_1000", "new_customer"]
        )
    ]


def make_loyalty_benefits() -> LoyaltyBenefits:
    return LoyaltyBenefits(
        points_earned=random.randint(50, 500),
        points_redeemed=random.randint(0, 100),
        tier_bonus_multiplier=round(random.uniform(1.0, 2.0), 1),
        cashback_percentage=round(random.uniform(0.01, 0.05), 2)
    )


def make_cart_value(subtotal: float) -> CartValue:
    taxes = make_tax_breakdown(subtotal)
    shipping = make_shipping_costs()
    discounts = make_discounts(subtotal)
    loyalty = make_loyalty_benefits()

    tax_total = sum(t.amount for t in taxes)
    discount_total = sum(d.discount_amount for d in discounts)
    shipping_total = shipping.base_shipping + shipping.expedited_fee + shipping.insurance

    final_total = round(subtotal + tax_total + shipping_total - discount_total, 2)

    return CartValue(
        subtotal=subtotal,
        tax_breakdown=taxes,
        shipping_costs=shipping,
        discounts_applied=discounts,
        loyalty_benefits=loyalty,
        final_total=final_total
    )

def make_billing_address() -> BillingAddress:
    return BillingAddress(
        address_hash=f"billing_{uuid.uuid4().hex[:8]}",
        country=random.choice(list(CountryCodeEnum)),
        postal_code=str(random.randint(10000, 99999)),
        address_type=random.choice(['residential', 'commercial', 'po_box'])
    )

def make_risk_signals() -> RiskSignals:
    return RiskSignals(
        first_time_payment=random.choice([True, False]),
        velocity_flag=random.choice([True, False]),
        geo_mismatch=random.choice([True, False]),
        fraud_score=round(random.uniform(0.01, 0.9), 2)
    )

def make_payment_method() -> PaymentMethod:
    return PaymentMethod(
        method_type=random.choice(list(PaymentMethodType)),
        provider=random.choice(list(ProviderEnum)),
        tokenized_identifier=f"token_{uuid.uuid4().hex[:6]}",
        billing_address=make_billing_address(),
        risk_signals=make_risk_signals()
    )

def make_shipping_address() -> ShippingAddress:
    return ShippingAddress(
        address_hash=f"shipping_{uuid.uuid4().hex[:8]}",
        same_as_billing=random.choice([True, False]),
        country=random.choice(list(CountryCodeEnum)),
        postal_code=str(random.randint(10000, 99999)),
        address_type=random.choice(['residential', 'commercial', 'po_box'])
    )


def make_shipping_method() -> ShippingMethod:
    return ShippingMethod(
        carrier=random.choice(['fedex', 'ups', 'usps', 'dhl']),
        service_level=random.choice(['ground', 'express', 'overnight', 'same_day']),
        estimated_delivery=datetime.utcnow() + timedelta(days=random.randint(1, 7)),
        tracking_enabled=True,
        signature_required=random.choice([True, False])
    )

def make_payment_context() -> PaymentContext:
    return PaymentContext(
        payment_methods=[make_payment_method()],
        shipping_context=ShippingContext(
            shipping_address=make_shipping_address(),
            shipping_method=make_shipping_method()
        )
    )