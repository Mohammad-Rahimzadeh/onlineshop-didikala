# Generated by Django 4.2.16 on 2024-10-10 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_account', '0004_favorite_favoriteproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteproduct',
            name='favorite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorites', to='app_account.favorite'),
        ),
    ]
