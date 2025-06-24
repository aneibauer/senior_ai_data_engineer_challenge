from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum
import random

from data_generator.models.interaction import (
    TouchpointJourney,
    TouchpointType,
    PageLoadMetrics,
    Coordinates,
    InteractionTypes,
    UserInteraction,
    PageTypes,
    PageContext,
    ActiveExperiment,
    ExperimentTypeEnum,
    ExperimentContext,
    FeatureFlag,
    InteractionContext
)


# -- Interaction Factories --

def make_touchpoint_journey(n=3) -> list[TouchpointJourney]:
    touchpoints = list(TouchpointType)
    return [
        TouchpointJourney(
            touchpoint=random.choice(touchpoints),
            timestamp=datetime.now() - timedelta(minutes=random.randint(1, 1000)),
            attribution_weight=round(random.uniform(0.1, 1.0), 2),
            campaign_id=f"cmp_{random.randint(100,999)}" if random.random() > 0.5 else None #optional campaign ID
        )
        for _ in range(n)
    ]

def make_page_load_metrics() -> PageLoadMetrics:
    return PageLoadMetrics(
        time_to_first_byte=random.randint(50, 500),
        first_contentful_paint=random.randint(100, 2000),
        largest_contentful_paint=random.randint(200, 3000),
        cumulative_layout_shift=round(random.uniform(0.0, 0.2), 3),
        first_input_delay=random.randint(10, 300)
    )

def make_coordinates() -> Coordinates:
    return Coordinates(
        x=random.randint(0, 1920),
        y=random.randint(0, 1080)
    )

def make_user_interaction(seq=1) -> UserInteraction:
    return UserInteraction(
        interaction_type=random.choice(list(InteractionTypes)),
        element_id=f"el_{random.randint(1000,9999)}",
        timestamp=datetime.now() - timedelta(seconds=random.randint(0, 3600)),
        coordinates=make_coordinates(),
        interaction_sequence=seq
    )

def make_user_interactions(n=5) -> list[UserInteraction]:
    return [make_user_interaction(seq=i+1) for i in range(n)]

def make_page_context() -> PageContext:
    return PageContext(
        page_type=random.choice(list(PageTypes)),
        page_url=f"https://example.com/{random.choice(['product', 'category', 'checkout', 'search'])}/{random.randint(1,1000)}",
        referrer_url=f"https://referrer.com/{random.choice(['ad', 'email', 'organic'])}",
        page_load_metrics=make_page_load_metrics(),
        user_interactions=make_user_interactions(random.randint(2, 7))
    )

def make_active_experiment() -> ActiveExperiment:
    return ActiveExperiment(
        experiment_id=f"exp_{random.randint(1000,9999)}",
        variant=f"treatment_{random.choice(['A', 'B', 'C'])}",
        allocation_timestamp=datetime.now() - timedelta(days=random.randint(0, 30)),
        experiment_type=random.choice(list(ExperimentTypeEnum))
    )

def make_active_experiments(n=2) -> list[ActiveExperiment]:
    return [make_active_experiment() for _ in range(n)]

def make_feature_flag() -> FeatureFlag:
    return FeatureFlag(
        flag_name=f"flag_{random.randint(1,10)}",
        enabled=random.choice([True, False]),
        variant=f"ml_model_v{random.randint(1, 5)}",
        rollout_percentage=random.randint(0, 100)
    )

def make_feature_flags(n=2) -> list[FeatureFlag]:
    return [make_feature_flag() for _ in range(n)]

def make_experiment_context() -> ExperimentContext:
    return ExperimentContext(
        active_experiments=make_active_experiments(random.randint(1, 3)),
        feature_flags=make_feature_flags(random.randint(1, 3))
    )

def make_interaction_context() -> InteractionContext:
    return InteractionContext(
        touchpoint_journey=make_touchpoint_journey(random.randint(1, 4)),
        page_context=make_page_context(),
        experiment_context=make_experiment_context()
    )
