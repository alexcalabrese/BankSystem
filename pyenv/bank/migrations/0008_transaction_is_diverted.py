# Generated by Django 4.0.5 on 2022-06-23 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0007_account_is_active_alter_transaction_account_from_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_diverted',
            field=models.BooleanField(default=0),
        ),
    ]
