# Generated by Django 5.0.6 on 2024-07-09 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=None, max_length=200, unique=True),
        ),
    ]
