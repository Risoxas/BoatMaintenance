# Generated by Django 4.1.3 on 2023-04-13 04:01

import boats.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Boat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('mooring_no', models.CharField(max_length=100)),
                ('mooring_location', models.CharField(max_length=200)),
                ('depth', models.IntegerField(blank=True, null=True)),
                ('last_check', models.DateField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('boat_image1', models.ImageField(default='', upload_to='images/')),
                ('boat_image2', models.ImageField(default='', upload_to='images/')),
                ('boat_image3', models.ImageField(default='', upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.BigAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('company_name', models.CharField(blank=True, max_length=200)),
                ('contact_first_name', models.CharField(max_length=50)),
                ('contact_last_name', models.CharField(max_length=50)),
                ('billing_address', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('state_province', models.CharField(blank=True, max_length=100)),
                ('postal_code', models.CharField(blank=True, max_length=5, validators=[django.core.validators.RegexValidator(code='invalid_postal_code', message='Postal code must be a 4 digit number', regex='^\\d{4}$')])),
                ('country', models.CharField(blank=True, max_length=50)),
                ('contact_title', models.CharField(blank=True, choices=[('Ms', 'Miss'), ('Mrs', 'Missus'), ('Mr', 'Mister'), ('Master', 'Master'), ('Dr', 'Doctor'), ('Fr', 'Father'), ('Rev', 'Reverend'), ('Atty', 'Attorney'), ('Hon', 'Honorable'), ('Prof', 'Professor'), ('Pres', 'President'), ('Vp', 'Vice President'), ('Gov', 'Governor'), ('Ofc', 'Office'), ('other', 'other')], default='other', max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('mobile_phone_number', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.BigAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('work_phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.BigAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('order_date', models.DateField()),
                ('service_date', models.DateField()),
                ('notes', models.TextField()),
                ('boat_image_pre1', models.ImageField(default='', upload_to='images/')),
                ('boat_info', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='boat_info', to='boats.boat')),
                ('boat_mooring_no', models.ForeignKey(db_column='mooring_no', on_delete=django.db.models.deletion.CASCADE, related_name='boat_mooring_no', to='boats.boat')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boats.customer')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boats.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.BigAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('product_name', models.CharField(max_length=100)),
                ('unit_price', boats.models.DollarField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order_Detail',
            fields=[
                ('order_detail_id', models.BigAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.FloatField()),
                ('unit_price', boats.models.DollarField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boats.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boats.product')),
            ],
        ),
        migrations.AddField(
            model_name='boat',
            name='customer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='boats.customer'),
        ),
    ]
