# Generated by Django 4.0.5 on 2022-06-19 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0006_selftransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='account_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='account_from', to='bank.account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='account_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='account_to', to='bank.account'),
        ),
    ]
