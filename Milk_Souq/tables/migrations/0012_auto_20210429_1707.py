# Generated by Django 3.1 on 2021-04-29 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0011_purchase_shoppingcart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='district',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='street',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
