# Generated by Django 3.1 on 2021-05-18 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0036_storeitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeitems',
            name='photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
