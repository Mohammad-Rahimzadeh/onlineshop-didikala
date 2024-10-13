# Generated by Django 4.0.4 on 2024-09-22 21:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('app_store', '0005_product_visit_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('body', models.TextField()),
                ('rate', models.PositiveIntegerField()),
                ('is_suggest', models.BooleanField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_published', models.BooleanField(default=False)),
                ('blog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_blog.blog')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products_comment', to='app_store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.BooleanField(choices=[(True, 'نقاط قوت'), (False, 'نقاط ضعف')])),
                ('description', models.TextField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_social.comment')),
            ],
        ),
        migrations.CreateModel(
            name='IsUsefull',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_useful', models.BooleanField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_social.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
    ]
