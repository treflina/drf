# Generated by Django 4.2.2 on 2023-07-30 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0004_alter_productimage_productline"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="product_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="product_type",
                to="product.producttype",
            ),
        ),
        migrations.AddField(
            model_name="productline",
            name="product_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="product",
                to="product.producttype",
            ),
        ),
        migrations.AddField(
            model_name="producttype",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="product.producttype",
            ),
        ),
        migrations.AlterField(
            model_name="productline",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="product_line_type",
                to="product.product",
            ),
        ),
    ]
