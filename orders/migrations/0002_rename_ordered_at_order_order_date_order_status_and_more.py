# Generated by Django 5.0.6 on 2024-07-09 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_alter_item_item_price_alter_item_stock_quantity_and_more'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ordered_at',
            new_name='order_date',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='배송 중', max_length=50),
        ),
        migrations.AlterModelTable(
            name='order',
            table='orders',
        ),
        migrations.CreateModel(
            name='Order_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
            options={
                'db_table': 'order_item',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='orders.Order_item', to='items.item'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
