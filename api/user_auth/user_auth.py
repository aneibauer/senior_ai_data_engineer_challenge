from fastapi import Header, HTTPException, status

# Mock users for simplicity
MOCK_USERS = {
    "admin-token": {"role": "admin", "tenant_id": None},
    "tenant1-token": {"role": "tenant", "tenant_id": "merchant_1"},
    "tenant2-token": {"role": "tenant", "tenant_id": "merchant_2"}
}

async def get_current_user(authorization: str = Header(...)):
    user = MOCK_USERS.get(authorization)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

def verify_tenant_access(user: dict, tenant_id: str):
    if user["role"] == "admin":
        return
    if user["role"] == "tenant" and user["tenant_id"] != tenant_id:
        raise HTTPException(status_code=403, detail="Access denied for this tenant.")