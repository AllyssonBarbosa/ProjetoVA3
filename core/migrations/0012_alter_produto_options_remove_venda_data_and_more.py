# Generated by Django 5.0.7 on 2024-09-16 12:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_venda_data_venda'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produto',
            options={},
        ),
        migrations.RemoveField(
            model_name='venda',
            name='data',
        ),
        migrations.AlterField(
            model_name='produto',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='data_venda',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
