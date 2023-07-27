import pytest

pytestmark = pytest.mark.django_db


class TestCategoryModels:

    def test_str_method(self, category_factory):
        obj = category_factory(name="test_cat")
        assert obj.__str__() == "test_cat"


class TestBrandModels:

    def test_str_method(self, brand_factory):
        obj = brand_factory(name="test_br")
        assert obj.__str__() == "test_br"


class TestProductModels:

    def test_str_method(self, product_factory):
        obj = product_factory(name="test_prod")
        assert obj.__str__() == "test_prod"
