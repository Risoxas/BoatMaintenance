# Generated by Django 4.1.3 on 2023-04-15 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boats', '0004_order_after_image1_order_after_image2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
