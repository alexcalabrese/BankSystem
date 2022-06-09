# Generated by Django 4.0.5 on 2022-06-09 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_alter_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.FloatField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.CharField(default='96bde148b3b464162a1f', editable=False, max_length=20, primary_key=True, serialize=False),
        ),
    ]
