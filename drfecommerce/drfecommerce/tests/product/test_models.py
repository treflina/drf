import pytest
from django.core.exceptions import ValidationError

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


class TestProductLineModel:

    def test_str_method(self, product_line_factory):
        obj = product_line_factory(sku="12345")
        assert obj.__str__() == "12345"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()


class TestProductImageModel:

    def test_str_method(self, product_image_factory):
        obj = product_image_factory(url="test.jpg")
        assert obj.__str__() == "test.jpg"


