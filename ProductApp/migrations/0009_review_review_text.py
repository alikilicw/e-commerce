# Generated by Django 4.1 on 2022-09-02 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0008_alter_review_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_text',
            field=models.TextField(null=True),
        ),
    ]
