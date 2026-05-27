import asyncio
import os
import sys

sys.path.insert(0, '.')
from services.tender_service.main import health as tender_health
from fastapi_gateway.main import health as gateway_health

async def test_health():
    # Test internal service health
    tender_status = await tender_health()
    print("Tender Service Health:", tender_status)
    
    # Mock SERVICES internally to allow the gateway health check to run
    # (Since we mocked the actual route we can just invoke it)
    from fastapi_gateway.main import SERVICES
    # For a real integration test we'd use TestClient, but gateway accesses it via httpx.
    # To be quick, we'll patch httpx or just use the local test
    import httpx
    # Normally the gateway reaches the tender service via HTTP. 
    gateway_status = await gateway_health()
    print("Gateway Health (disconnected proxy):", gateway_status)

asyncio.run(test_health())
