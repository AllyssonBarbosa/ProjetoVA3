# Generated by Django 4.2.4 on 2023-08-13 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_produto_dia_de_venda_produto_descricao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venda',
            old_name='data',
            new_name='data_venda',
        ),
        migrations.AddField(
            model_name='venda',
            name='valor_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
