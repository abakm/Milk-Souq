# Generated by Django 3.1 on 2021-04-27 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0002_item_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
