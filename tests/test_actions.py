import pytest
@pytest.mark.asyncio
async def test_ingest(client):
    r = await client.post("/api/actions/ingest", json={"title": "Standup", "notes": "Sam will send the proposal by Friday. Alex to fix auth."})
    assert r.status_code == 200
    assert len(r.json()["actions"]) >= 1
