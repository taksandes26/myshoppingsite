# Generated by Django 5.0.6 on 2024-07-06 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_moblile_profile_mobile_remove_profile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=models.CharField(max_length=10),
        ),
    ]