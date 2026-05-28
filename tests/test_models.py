"""Tests for recommendation models."""

import numpy as np
import pytest 

from recsys.models import ModelFactory, PopularityRecommender
from recsys.models.base import BaseRecommender


def test_factory_registers_popularity() -> None:
    """Factory should have popularity model registered."""
    assert "popularity" in ModelFactory.list_models()


def test_factory_creates_popularity() -> None:
    """Factory should create PopularityRecommender instance."""
    model = ModelFactory.create("popularity")
    assert isinstance(model, PopularityRecommender)


def test_factory_raises_for_unknown_model() -> None:
    """Factory should raise ValueError for unregistered model."""
    with pytest.raises(ValueError, match="not found"):
        ModelFactory.create("unknown_model")


def test_popularity_recommender_fit() -> None:
    """PopularityRecommender should fit without errors."""
    model = ModelFactory.create("popularity")
    matrix = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 0]], dtype=np.float32)
    model.fit(matrix)
    assert model._popular_items is not None


def test_popularity_recommender_recommend() -> None:
    """PopularityRecommender should return correct number of items."""
    model = ModelFactory.create("popularity")
    matrix = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 0]], dtype=np.float32)
    model.fit(matrix)
    recs = model.recommend(user_id=0, top_k=2)
    assert len(recs) == 2


def test_popularity_recommender_ranking() -> None:
    """PopularityRecommender should rank items by popularity."""
    model = ModelFactory.create("popularity")
    matrix = np.array([[1, 0, 0], [1, 0, 0], [1, 1, 0]], dtype=np.float32)
    model.fit(matrix)
    recs = model.recommend(user_id=0, top_k=3)
    assert recs[0] == 0


def test_base_recommender_is_abstract() -> None:
    """BaseRecommender should not be instantiable directly."""
    with pytest.raises(TypeError):
        BaseRecommender()
