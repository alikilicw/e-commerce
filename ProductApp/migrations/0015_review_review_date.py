# Generated by Django 4.1 on 2022-09-03 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0014_remove_currency_currency_dollar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
