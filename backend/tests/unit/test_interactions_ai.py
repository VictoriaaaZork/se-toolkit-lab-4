"""AI-generated (curated) unit tests for interaction filtering logic.

These tests target edge/boundary cases not fully covered by the base suite.
"""

from datetime import datetime

from app.models.interaction import InteractionLog
from app.routers.interactions import filter_by_max_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(
        id=id,
        learner_id=learner_id,
        item_id=item_id,
        kind="attempt",
        created_at=datetime.now(),
    )


# KEPT: covers edge case where max_item_id is negative; should filter out all non-negative item_id values.
def test_filter_with_negative_max_item_id_returns_empty() -> None:
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=-1)
    assert result == []


# KEPT: ensures boundary is inclusive for multiple interactions with item_id == max_item_id.
def test_filter_includes_multiple_interactions_at_boundary() -> None:
    interactions = [_make_log(1, 1, 2), _make_log(2, 2, 2), _make_log(3, 3, 3)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=2)
    assert [i.id for i in result] == [1, 2]


# FIXED: verifies stable ordering is preserved (filter should not reorder items).
def test_filter_preserves_original_order() -> None:
    interactions = [_make_log(1, 1, 2), _make_log(2, 2, 1), _make_log(3, 3, 2)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=2)
    assert [i.id for i in result] == [1, 2, 3]


# FIXED: verifies max_item_id == 0 includes item_id == 0 and excludes positive item_id values.
def test_filter_with_zero_max_item_id_includes_zero() -> None:
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
    assert [i.id for i in result] == [1]


# DISCARDED: duplicates the already-required boundary test (item_id == max_item_id) in the main test file.
# def test_filter_boundary_duplicate() -> None:
#     interactions = [_make_log(1, 1, 2)]
#     result = filter_by_max_item_id(interactions=interactions, max_item_id=2)
#     assert len(result) == 1
