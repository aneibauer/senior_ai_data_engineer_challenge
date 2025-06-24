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
    timeframe: str = Query("5m", description="Timeframe for the metrics, e.g., '5m' for last 5 minutes."),
    user: dict = Depends(get_current_user)
):

    #enforce tenant access. Denies access if user does not have access to the tenant data
    verify_tenant_access(user, tenant_id)

    delta = parse_timeframe(timeframe)

    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=delta)

    #TODO: figure out actual timestamp field in the events table to filter by
    query = """
        SELECT tenant_id, COUNT(1) as event_count
        FROM commerce_events_table
        WHERE tenant_id = :tenant_id
          AND event_metadata ->> 'timestamp' BETWEEN :start_time AND :end_time
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