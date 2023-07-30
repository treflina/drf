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

    def test_str_method(self, product_line_factory, attribute_value_factory):
        attr = attribute_value_factory(attribute_value="test")
        obj = product_line_factory(sku="12345", attribute_value=(attr,))
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


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        test = attribute_factory(name="test")
        obj = product_type_factory.create(name="test_type", attribute=(test,))
        # we pass reference to the link table that is used in @factory.post_generation
        # x = ProductTypeAttribute.objects.get(id=1)
        # print(x)

        assert obj.__str__() == "test_type"


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        obj = attribute_factory(name="test_attribute")
        assert obj.__str__() == "test_attribute"


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory, attribute_factory):
        obj_a = attribute_factory(name="test_attribute")
        obj_b = attribute_value_factory(attribute_value="test_value", attribute=obj_a)
        assert obj_b.__str__() == "test_attribute-test_value"


