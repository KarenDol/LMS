# Generated by Django 4.2.7 on 2024-09-02 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_manager", "0004_contract_sign_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="parent",
            name="Address",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
