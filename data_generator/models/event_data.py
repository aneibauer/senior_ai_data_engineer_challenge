from pydantic import BaseModel
from typing import Literal
from enum import Enum
from data_generator.models.user import UserContext
from data_generator.models.business import BusinessContext
from data_generator.models.interaction import InteractionContext

class EventType(Enum):
    USER_INTERACTION = "user_interaction"
    TRANSACTION = "transaction"
    SYSTEM_EVENT = "system_event"
    ML_INFERENCE = "ml_inference"
    
class EventSubType(Enum):
    PAGE_VIEW = "page_view"
    PURCHASE = "purchase"
    FRAUD_SCORE = "fraud_score"
    RECOMMENDATION_CLICK = "recommendation_click"

class EventData(BaseModel):
    event_type: EventType
    event_subtype: EventSubType
    user_context: UserContext
    business_context: BusinessContext
    interaction_context: InteractionContext