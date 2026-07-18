"""Endpoint tests for the merchandise API (prefix ``/api``)."""


def _sample(**overrides):
    data = {"name": "Indomie Goreng", "category_id": 1, "price": 3000, "stock": 50}
    data.update(overrides)
    return data


def test_create_merchandise(client):
    resp = client.post("/api/merchandises", json=_sample())
    assert resp.status_code == 201
    assert resp.json() == {"message": "New data created"}


def test_create_merchandise_validation_error(client):
    resp = client.post("/api/merchandises", json={"name": "Missing fields"})
    assert resp.status_code == 422


def test_list_merchandise_empty(client):
    resp = client.get("/api/merchandise")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_merchandise_after_create(client):
    client.post("/api/merchandises", json=_sample())
    client.post("/api/merchandises", json=_sample(name="Aqua", category_id=2, price=4000))

    resp = client.get("/api/merchandise")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 2
    assert {m["name"] for m in body} == {"Indomie Goreng", "Aqua"}


def test_get_merchandise_by_id(client):
    client.post("/api/merchandises", json=_sample())

    resp = client.get("/api/merchandise/1")
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == 1
    assert body["name"] == "Indomie Goreng"
    assert body["price"] == 3000


def test_get_merchandise_not_found(client):
    resp = client.get("/api/merchandise/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Merchandise not found"


def test_search_by_name(client):
    client.post("/api/merchandises", json=_sample(name="Indomie Goreng"))
    client.post("/api/merchandises", json=_sample(name="Aqua", category_id=2))

    resp = client.get("/api/merchandise/search/", params={"name": "Indomie"})
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 1
    assert body[0]["name"] == "Indomie Goreng"


def test_search_by_category(client):
    client.post("/api/merchandises", json=_sample(name="Indomie Goreng", category_id=1))
    client.post("/api/merchandises", json=_sample(name="Aqua", category_id=2))

    resp = client.get("/api/merchandise/search/", params={"category": 2})
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 1
    assert body[0]["name"] == "Aqua"


def test_update_merchandise(client):
    client.post("/api/merchandises", json=_sample())

    resp = client.put(
        "/api/merchandise/1",
        json=_sample(name="Indomie Goreng Jumbo", price=3500, stock=40),
    )
    assert resp.status_code == 200
    assert resp.json() == {"message": "Merchandise updated"}

    updated = client.get("/api/merchandise/1").json()
    assert updated["name"] == "Indomie Goreng Jumbo"
    assert updated["price"] == 3500
    assert updated["stock"] == 40


def test_update_merchandise_not_found(client):
    resp = client.put("/api/merchandise/999", json=_sample())
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Merchandise not found"


def test_delete_merchandise(client):
    client.post("/api/merchandises", json=_sample())

    resp = client.delete("/api/merchandise/1")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Merchandise deleted"}

    assert client.get("/api/merchandise/1").status_code == 404


def test_delete_merchandise_not_found(client):
    resp = client.delete("/api/merchandise/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Merchandise not found"
