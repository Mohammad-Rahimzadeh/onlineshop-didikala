# Generated by Django 4.0.4 on 2024-10-06 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0005_product_visit_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.CharField(default='Didikala', max_length=255),
        ),
    ]
