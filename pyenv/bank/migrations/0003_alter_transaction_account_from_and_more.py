# Generated by Django 4.0.5 on 2022-06-12 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_alter_account_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='account_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='account_from', to='bank.account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='account_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='account_to', to='bank.account'),
        ),
    ]