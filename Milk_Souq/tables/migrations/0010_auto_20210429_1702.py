# Generated by Django 3.1 on 2021-04-29 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0009_auto_20210429_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='itid',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='pid',
        ),
        migrations.DeleteModel(
            name='purchase',
        ),
        migrations.DeleteModel(
            name='shoppingcart',
        ),
    ]
