# Generated by Django 4.1.1 on 2022-10-06 20:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ProductApp', '0017_product_fav_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='fav_user',
            field=models.ManyToManyField(blank=True, related_name='fav_user', to=settings.AUTH_USER_MODEL),
        ),
    ]