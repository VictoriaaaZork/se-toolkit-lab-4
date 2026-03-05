"""End-to-end tests for the GET /interactions endpoint."""


def test_get_interactions_returns_200(client) -> None:
    r = client.get("/interactions/")
    assert r.status_code == 200


def test_get_interactions_response_items_have_expected_fields(client) -> None:
    r = client.get("/interactions/")
    assert r.status_code == 200

    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0

    first = data[0]
    assert set(first.keys()) >= {"id", "item_id", "created_at"}


def test_get_interactions_filter_includes_boundary(client) -> None:
    r = client.get("/interactions/?max_item_id=1")
    assert r.status_code == 200

    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0

    assert all(item["item_id"] <= 1 for item in data)
