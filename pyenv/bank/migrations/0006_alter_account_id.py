# Generated by Django 4.0.5 on 2022-06-09 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_alter_account_balance_alter_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.CharField(default='a13bb8462f8d5dfbd733', editable=False, max_length=20, primary_key=True, serialize=False),
        ),
    ]
