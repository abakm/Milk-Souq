# Generated by Django 3.1 on 2021-05-05 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0019_auto_20210504_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyitem',
            name='photo',
            field=models.ImageField(null=True, upload_to='items/'),
        ),
    ]
