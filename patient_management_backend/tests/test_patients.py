import pytest
from httpx import AsyncClient
from schemas.patient import PatientCreate, PatientUpdate

@pytest.mark.asyncio
async def test_create_patient(client: AsyncClient):
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "gender": "male"
    }
    response = await client.post("/api/patients/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["phone"] == payload["phone"]
    assert data["gender"] == payload["gender"]
    global patient_id
    patient_id = data["id"]

@pytest.mark.asyncio
async def test_get_patient(client: AsyncClient):
    response = await client.get(f"/api/patients/{patient_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == patient_id

@pytest.mark.asyncio
async def test_update_patient(client: AsyncClient):
    payload = {"first_name": "Jane"}
    response = await client.put(f"/api/patients/{patient_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"

@pytest.mark.asyncio
async def test_list_patients(client: AsyncClient):
    response = await client.get("/api/patients/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(p["id"] == patient_id for p in data)

@pytest.mark.asyncio
async def test_delete_patient(client: AsyncClient):
    response = await client.delete(f"/api/patients/{patient_id}")
    assert response.status_code == 204
    # Confirm deletion
    response = await client.get(f"/api/patients/{patient_id}")
    assert response.status_code == 404
