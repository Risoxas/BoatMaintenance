# Generated by Django 4.1.6 on 2023-04-09 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boats', '0007_alter_boats_boat_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boats',
            name='boat_image',
            field=models.ImageField(default='', upload_to='images'),
        ),
    ]