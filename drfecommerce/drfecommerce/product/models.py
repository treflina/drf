from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from .fields import OrderField


class IsActiveQuerySet(models.QuerySet):
    # ver3
    def isactive(self):
        return self.filter(is_active=True)


# class ActiveManager(models.Manager):
# we add a func that we can call or not, not overriding anything (ver2)
# def isactive(self):
#     return self.get_queryset().filter(is_active=True)
# ver1
# def get_queryset(self):
#     return super().get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = IsActiveQuerySet.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    pid = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey(
        "Category", on_delete=models.PROTECT
    )
    is_active = models.BooleanField(default=False)
    product_type = models.ForeignKey(
        "ProductType",
        on_delete=models.PROTECT,
        related_name="product_type",
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    attribute_value = models.ManyToManyField(
        "AttributeValue",
        through="ProductAttributeValue",
        related_name="product_attr_value",
    )

    objects = IsActiveQuerySet.as_manager()
    # objects = models.Manager()
    # objects = ActiveManager()

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_value"
    )

    def __str__(self):
        return f"{self.attribute.name}-{self.attribute_value}"


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=10)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        "Product", on_delete=models.PROTECT, related_name="product_line_type"
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True)
    objects = IsActiveQuerySet.as_manager()
    weight = models.FloatField()
    product_type = models.ForeignKey(
        "ProductType",
        on_delete=models.PROTECT,
        related_name="product",
        null=True,
    )
    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_value",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate values.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=255)
    url = models.ImageField(upload_to=None, default="test.jpg")
    productline = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="productline", blank=True)

    def clean(self):
        qs = ProductImage.objects.filter(productline=self.productline)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate values.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.productline.sku}_img"


class ProductAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_value_av",
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_value_pl"
    )

    class Meta:
        unique_together = ("attribute_value", "product")

    # def clean(self):
    #     qs = (
    #         ProductLineAttributeValue.objects.filter(
    #             attribute_value=self.attribute_value
    #         )
    #         .filter(product_line=self.product_line)
    #         .exists()
    #     )
    #     print("qs", qs)
    #     if not qs:
    #         iqs = Attribute.objects.filter(
    #             attribute_value__product_line_attribute_value=self.product_line
    #         ).values_list("pk", flat=True)
    #         if self.attribute_value.attribute.id in list(iqs):
    #             raise ValidationError("Duplicate attribute exists.")

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     return super(ProductLineAttributeValue, self).save(*args, **kwargs)


class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_av",
    )
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_attribute_value_pl"
    )

    class Meta:
        unique_together = ("attribute_value", "product_line")

    def clean(self):
        qs = (
            ProductLineAttributeValue.objects.filter(
                attribute_value=self.attribute_value
            )
            .filter(product_line=self.product_line)
            .exists()
        )
        print("qs", qs)
        if not qs:
            iqs = Attribute.objects.filter(
                attribute_value__product_line_attribute_value=self.product_line
            ).values_list("pk", flat=True)
            if self.attribute_value.attribute.id in list(iqs):
                raise ValidationError("Duplicate attribute exists.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLineAttributeValue, self).save(*args, **kwargs)


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    attribute = models.ManyToManyField(
        Attribute, through="ProductTypeAttribute", related_name="product_type_attribute"
    )

    def __str__(self):
        return str(self.name)


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="product_type_attribute_pt"
    )
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="product_type_attribute_a"
    )

    class Meta:
        unique_together = ("attribute", "product_type")
