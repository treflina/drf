import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from drfecommerce.product.models import Category, Product

pytestmark = pytest.mark.django_db


class TestCategoryModels:
    def test_str_method(self, category_factory):
        obj = category_factory(name="test_cat")
        assert obj.__str__() == "test_cat"

    def test_name_max_length(self, category_factory):
        name = "x" * 236
        obj = category_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_name_unique_field(self, category_factory):
        category_factory(name="test-name")
        with pytest.raises(IntegrityError):
            category_factory(name="test-name")

    def test_slug_unique_field(self, category_factory):
        category_factory(slug="test-name")
        with pytest.raises(IntegrityError):
            category_factory(slug="test-name")

    def test_isactive_default_false(self, category_factory):
        obj = category_factory()
        assert obj.is_active is True

    def test_parent_category_ondelete_protect(self, category_factory):
        obj1 = category_factory()
        category_factory(parent=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_parent_field_null(self, category_factory):
        obj1 = category_factory()
        assert obj1.parent is None

    def test_return_category_active_only_true(self, category_factory):
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.isactive().count()
        assert qs == 1

    def test_return_category_active_only_false(self, category_factory):
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.count()
        assert qs == 2


class TestProductModels:
    def test_str_method(self, product_factory):
        obj = product_factory(name="test_prod")
        assert obj.__str__() == "test_prod"

    def test_name_max_length(self, product_factory):
        name = "x" * 236
        obj = product_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_pid_max_length(self, product_factory):
        pid = "x" * 11
        obj = product_factory(pid=pid)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_is_digital_false_default(self, product_factory):
        obj = product_factory(name="nodigital")
        assert obj.is_digital is False

    def test_name_unique_field(self, product_factory):
        product_factory(name="test-name")
        with pytest.raises(IntegrityError):
            product_factory(name="test-name")

    def test_fk_category_ondelete_protect(self, category_factory, product_factory):
        cat1 = category_factory()
        product_factory(category=cat1)
        with pytest.raises(IntegrityError):
            cat1.delete()

    def test_return_product_active_only_true(self, product_factory):
        product_factory(is_active=True)
        product_factory(is_active=False)
        qs = Product.objects.isactive().count()
        assert qs == 1

    def test_return_product_active_only_false(self, product_factory):
        product_factory(is_active=True)
        product_factory(is_active=False)
        qs = Product.objects.count()
        assert qs == 2


class TestProductLineModel:
    def test_duplicate_attribute_inserts(
        self,
        product_line_factory,
        attribute_factory,
        attribute_value_factory,
        product_line_attribute_value_factory,
    ):
        obj1 = attribute_factory(name="shoe-color")
        obj2 = attribute_value_factory(attribute_value="red", attribute=obj1)
        obj3 = attribute_value_factory(attribute_value="blue", attribute=obj1)
        obj4 = product_line_factory()
        product_line_attribute_value_factory(attribute_value=obj2, product_line=obj4)
        with pytest.raises(ValidationError):
            product_line_attribute_value_factory(
                attribute_value=obj3, product_line=obj4
            )

    def test_str_method(self, product_line_factory):
        # attr = attribute_value_factory(attribute_value="test")
        # obj = product_line_factory(sku="12345", attribute_value=(attr,))
        obj = product_line_factory(sku="12345")
        assert obj.__str__() == "12345"

    def test_fk_product_type_on_delete_protect(
        self, product_type_factory, product_line_factory
    ):
        obj1 = product_type_factory()
        product_line_factory(product_type=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()

    def test_field_decimal_places(self, product_line_factory):
        price = 1.001
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_field_price_max_digits(self, product_line_factory):
        price = 1111.00
        with pytest.raises(ValidationError):
            product_line_factory(price=price)


class TestProductImageModel:
    def test_str_method(self, product_image_factory, product_line_factory):
        obj1 = product_line_factory(sku="12345")
        obj = product_image_factory(url="test.jpg", productline=obj1)
        assert obj.__str__() == "12345_img"


class TestProductTypeModel:
    def test_str_method(self, product_type_factory):
        # test = attribute_factory(name="test")
        # obj = product_type_factory.create(name="test_type", attribute=(test,))
        obj = product_type_factory.create(name="test_type")
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
