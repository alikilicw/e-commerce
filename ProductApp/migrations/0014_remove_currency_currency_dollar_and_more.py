# Generated by Django 4.1 on 2022-09-03 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0013_currency_product_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='currency_Dollar',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='currency_Euro',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='currency_TL',
        ),
        migrations.AddField(
            model_name='currency',
            name='currency_symbol',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='currency',
            name='currency_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ProductApp.currency'),
        ),
    ]