from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


# --- Touchpoint Attribution ---

class TouchpointJourney(BaseModel):
    touchpoint: str
    timestamp: datetime
    attribution_weight: float
    campaign_id: Optional[str] = None  # Present for things like email campaigns


# --- Page Context ---

class PageLoadMetrics(BaseModel):
    time_to_first_byte: int
    first_contentful_paint: int
    largest_contentful_paint: int
    cumulative_layout_shift: float
    first_input_delay: int


class Coordinates(BaseModel):
    x: int
    y: int

class InteractionTypes(Enum):
    CLICK = 'click'
    SCROLL = 'scroll'
    HOVER = 'hover'
    FORM_INPUT = 'form_input'

class UserInteraction(BaseModel):
    interaction_type: InteractionTypes
    element_id: str
    timestamp: datetime
    coordinates: Coordinates
    interaction_sequence: int

class PageTypes(Enum):
    PRODUCT_DETAIL = 'product_detail'
    CATEGORY = 'category'
    CHECKOUT = 'checkout'
    SEARCH_RESULTS = 'search_results'
    OTHER = 'other'

class PageContext(BaseModel):
    page_type: PageTypes
    page_url: str
    referrer_url: str
    page_load_metrics: PageLoadMetrics
    user_interactions: List[UserInteraction]


# --- Experiment Context ---
class ExperimentTypeEnum(Enum):
    UI_TEST = 'ui_test'
    FEATURE_FLAG = 'feature_flag'
    ALGORITHM_TEST = 'algorithm_test'

class ActiveExperiment(BaseModel):
    experiment_id: str
    variant: str
    allocation_timestamp: datetime
    experiment_type: ExperimentTypeEnum


class FeatureFlag(BaseModel):
    flag_name: str
    enabled: bool
    variant: str
    rollout_percentage: int = Field(ge=0, le=100)  # Percentage of users for whom the flag is enabled


class ExperimentContext(BaseModel):
    active_experiments: List[ActiveExperiment]
    feature_flags: List[FeatureFlag]


# --- Full Interaction Context ---

class InteractionContext(BaseModel):
    touchpoint_journey: List[TouchpointJourney]
    page_context: PageContext
    experiment_context: ExperimentContext