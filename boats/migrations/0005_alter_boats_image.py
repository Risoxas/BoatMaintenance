# Generated by Django 4.1.6 on 2023-04-05 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boats', '0004_alter_boats_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boats',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]