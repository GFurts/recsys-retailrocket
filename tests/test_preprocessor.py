"""Tests for data preprocessing module."""

import pandas as pd
from recsys.data.preprocessor import encode_ids, filter_events


def make_sample_df() -> pd.DataFrame:
    """Create a sample events dataframe for testing."""
    users = [1] * 5 + [2] * 5
    items = [10, 20, 30, 40, 50] * 2
    return pd.DataFrame(
        {
            "visitorid": users,
            "itemid": items,
            "event": ["view"] * 10,
        }
    )


def test_filter_events_removes_low_interactions() -> None:
    """Users with fewer than min_interactions should be removed."""
    df = make_sample_df()
    filtered = filter_events(df, min_interactions=5)
    assert 3 not in filtered["visitorid"].values


def test_filter_events_keeps_active_users() -> None:
    """Users with enough interactions should be kept."""
    df = make_sample_df()
    filtered = filter_events(df, min_interactions=2)
    assert 1 in filtered["visitorid"].values
    assert 2 in filtered["visitorid"].values


def test_encode_ids_creates_sequential_indices() -> None:
    """Encoded user and item indices should be sequential integers."""
    df = make_sample_df()
    filtered = filter_events(df, min_interactions=2)
    encoded, user_enc, item_enc = encode_ids(filtered)
    assert encoded["user_idx"].min() == 0
    assert encoded["item_idx"].min() == 0


def test_encode_ids_returns_encoders() -> None:
    """encode_ids should return user and item encoder dicts."""
    df = make_sample_df()
    filtered = filter_events(df, min_interactions=2)
    _, user_enc, item_enc = encode_ids(filtered)
    assert isinstance(user_enc, dict)
    assert isinstance(item_enc, dict)
    assert len(user_enc) == 2
