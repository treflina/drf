import factory

from drfecommerce.product.models import (
    Brand,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductType,
    ProductTypeAttribute,
    Attribute,
    AttributeValue
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: "test_category_%d" % n)
    slug = factory.Sequence(lambda n: "test_slug_%d" % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f"Brand_{n}")


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = "attribute_name_test"
    description = "attr_description_test"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = "test_type"

    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = "test_product"
    slug = "test_sluggy"
    description = "test_description"
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)


class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute_value = "attr_test"
    attribute = factory.SubFactory(AttributeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.00
    sku = "0123456789"
    stock_qty = 1
    product = factory.SubFactory(ProductFactory)
    is_active = True

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)
        


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = "sample text"
    url = "test.jpg"
    productline = factory.SubFactory(ProductLineFactory)


