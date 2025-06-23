from pydantic import BaseModel, BeforeValidator, Field
from typing import List, Optional, Annotated, Literal
from datetime import datetime, timedelta
import uuid
from enum import Enum
import random

from data_generator.models.user import CountryCodeEnum
from data_generator.models.business import (
    Verticals, CATEGORY_TREE, CurrencyEnum, AvailabilityStatus, ColorEnum,
    ProductHierarchy, Pricing, Inventory, ProductAttributes, Dimensions,
    PerformanceMetrics, Product, TaxBreakdown, ShippingCosts, Discount,
    LoyaltyBenefits, CartValue, BillingAddress, RiskSignals, PaymentMethod,
    PaymentMethodType, ProviderEnum, ShippingAddress, ShippingMethod,
    ShippingContext, PaymentContext, CartContext, TransactionContext,
    TenantMetadata, BusinessContext
)


# -- Business Factory Functions --

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
    discount_value = round(random.uniform(0.05, 0.50),3)  # Discount between 5% and 50%
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
        estimated_delivery=datetime.now() + timedelta(days=random.randint(1, 7)),
        tracking_enabled=random.choice([True, False]),
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

def make_cart_context() -> CartContext:
    # Generate a random subtotal based on the sum of product sale prices
    products = make_products()
    subtotal = sum(p.pricing.sale_price for p in products)
    cart_value = make_cart_value(subtotal)
    payment_context = make_payment_context()
    return CartContext(
        cart_id=f"cart_{uuid.uuid4().hex[:8]}",
        cart_value=cart_value,
        payment_context=payment_context
    )

def make_transaction_context() -> TransactionContext:
    products = make_products()
    # Use the same products to calculate subtotal for cart context
    subtotal = sum(p.pricing.sale_price for p in products)
    cart_value = make_cart_value(subtotal)
    payment_context = make_payment_context()
    cart_context = CartContext(
        cart_id=f"cart_{uuid.uuid4().hex[:8]}",
        cart_value=cart_value,
        payment_context=payment_context
    )
    return TransactionContext(
        products=products,
        cart_context=cart_context
    )

def make_tenant_metadata() -> TenantMetadata:
    return TenantMetadata(
        merchant_id=f"merchant_{uuid.uuid4().hex[:8]}",
        merchant_tier=random.choice(['enterprise', 'standard', 'startup']),
        industry_vertical=random.choice(list(Verticals)),
        geographic_markets=random.sample(list(CountryCodeEnum), k=random.randint(1, 3)),
        business_model=random.choice(['b2c', 'b2b', 'marketplace', 'subscription'])
    )

def make_business_context() -> BusinessContext:
    return BusinessContext(
        tenant_metadata=make_tenant_metadata(),
        transaction_context=make_transaction_context()
    )



# if __name__ == "__main__":
    # hierarchy = make_product_hierarchy()
    # print(hierarchy.model_dump_json(indent=2))  # Print the product hierarchy in a readable JSON form

    # pricing = make_pricing()
    # print(pricing.model_dump_json(indent=2))  # Print the pricing in a readable JSON form

    # inventory = make_inventory()
    # print(inventory.model_dump_json(indent=2))  # Print the inventory in a readable JSON form

    # attributes = make_product_attributes()
    # print(attributes.model_dump_json(indent=2))  # Print the product attributes in a readable JSON form

    # performance = make_performance_metrics()
    # print(performance.model_dump_json(indent=2))  # Print the performance metrics in a readable JSON form

    # product = make_product()
    # print(product.model_dump_json(indent=2))  # Print the full product in a readable JSON form   

    # products = make_products()
    # print([p.model_dump_json(indent=2) for p in products])  # Print the list of products in a readable JSON form

    # cart_value = make_cart_value(100.0)
    # print(cart_value.model_dump_json(indent=2))  # Print the cart value breakdown

    # payment_context = make_payment_context()
    # print(payment_context.model_dump_json(indent=2))  # Print the payment context in a readable JSON form

    # billing_address = make_billing_address()
    # print(billing_address.model_dump_json(indent=2))  # Print the billing address 

    # shipping_address = make_shipping_address()
    # print(shipping_address.model_dump_json(indent=2))  # Print the shipping address

    # risk_signals = make_risk_signals()
    # print(risk_signals.model_dump_json(indent=2))  # Print the risk signals

    # shipping_method = make_shipping_method()
    # print(shipping_method.model_dump_json(indent=2))  # Print the shipping method

    # cart_context = make_cart_context()
    # print(cart_context.model_dump_json(indent=2))  # Print the cart context in a readable JSON form

    # transaction_context = make_transaction_context()
    # print(transaction_context.model_dump_json(indent=2))  # Print the transaction context in a readable JSON form

    # tenant_metadata = make_tenant_metadata()
    # print(tenant_metadata.model_dump_json(indent=2))  # Print the tenant metadata

    #all of this works well!
    # business_context = make_business_context()
    # print(business_context.model_dump_json(indent=2))  # Print the full business context