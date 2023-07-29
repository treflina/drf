import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import (
    BrandFactory,
    CategoryFactory,
    ProductImageFactory,
    ProductFactory,
    ProductLineFactory,
)

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)


@pytest.fixture
def api_client():
    return APIClient
