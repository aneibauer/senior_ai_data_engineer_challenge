"""
routers/analytics.py

Real-Time Analytics API Router Module

This module implements the core real-time analytics endpoints (currently limited to one) 
for the analytics API platform. 

Key Features:
- Real-time metrics aggregation with configurable timeframes for data retrieval
- Multi-tenant data isolation and access control (using mock authentication for simplicity)
- Flexible timeframe parsing (minutes, hours, days)
- Asynchronous database operations for optimal performance and scalability
- Framework to implement future enterprise-grade authentication and authorization

The module serves as the primary interface for stakeholders to retrieve analytics
data from their event streams, supporting the platform's goal of handling 10K+ concurrent
requests with horizontal autoscaling capabilities.

Current Implementation:
- GET /api/v2/analytics/realtime/metrics: Retrieves aggregated event counts for a tenant
  within a specified timeframe, with proper access control and validation
    - Parameters:
      - tenant_id: The ID of the tenant to filter events on
      - timeframe: The time period for which to retrieve metrics (default is '1d' for last 1 day)
    - Returns:
      - JSON response with tenant ID, event count, and timeframe

Future Enhancements:
- WebSocket streaming endpoints, allowing for real-time updates and data availability
- Optimization for query performance via result-caching and pre-aggregation (spark applications)
- Custom dashboard generation capabilities
- Implementing advanced authentication and authorization mechanisms
- Add additional routers and endpoints for more analytics features

*This setup is robust to prevent sql injection attacks and ensures that only authorized users
can access their respective tenant data. The use of async database operations allows for high concurrency
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta

from db.postgres import database
from models.api_models import RealTimeMetricsResponse
from user_auth.user_auth import get_current_user, verify_tenant_access #uses mock authentication for simplicity for now

def parse_timeframe(timeframe: str) -> int:
    """
    Converts a string timeframe like '5m', '2h', or '1d' into minutes.
    Returns the number of minutes as an int.
    Raises HTTPException if invalid format.
    """
    if timeframe.endswith("h"):
        unit = 60
        value = timeframe[:-1]
    elif timeframe.endswith("m"):
        unit = 1
        value = timeframe[:-1]
    elif timeframe.endswith("d"):
        unit = 1440
        value = timeframe[:-1]
    else:
        raise HTTPException(status_code=400, detail="Invalid timeframe format. Use like '5m', '2h', '1d'.")

    try:
        return int(value) * unit
    except ValueError:
        raise HTTPException(status_code=400, detail="Timeframe value must be a number.")
    

router = APIRouter(
    prefix="/api/v2/analytics/realtime",
    tags=["Real-time Analytics"]
)

@router.get("/metrics", response_model=RealTimeMetricsResponse)
async def get_realtime_metrics(
    tenant_id: str = Query(..., description="The tenant ID to filter events on."),
    timeframe: str = Query("1d", description="Timeframe for the metrics, e.g., '1d' for last 1 day(s)."),
    user: dict = Depends(get_current_user)
) -> RealTimeMetricsResponse:

    #enforce customer access. Denies access if user doesn't have correct token or tenant_id doesn't match
    verify_tenant_access(user, tenant_id)

    delta_minutes = parse_timeframe(timeframe)

    #TODO: allow custom start and end times for filtering instead of just using the last X minutes
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=delta_minutes)

    query = """
        SELECT tenant_id, COUNT(1) as event_count
        FROM commerce_events_table
        WHERE tenant_id = :tenant_id
          AND timestamp BETWEEN :start_time AND :end_time
        GROUP BY tenant_id
    """

    values = {
        "tenant_id": tenant_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }

    result = await database.fetch_one(query=query, values=values)

    if not result:
        raise HTTPException(status_code=404, detail="No events found for tenant.")

    return {
        "tenant_id": result["tenant_id"],
        "event_count": result["event_count"],
        "timeframe": timeframe
    }