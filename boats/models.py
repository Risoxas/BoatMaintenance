from django.db import models
from django.utils.html import mark_safe
from django.core.validators import RegexValidator, MinLengthValidator, MaxValueValidator, MinValueValidator
from django import forms
from django.contrib import admin
import datetime

postal_validator = RegexValidator(
    regex=r'^\d{4}$', message='Postal code must be a 4 digit number', code='invalid_postal_code')

number_validator = RegexValidator(regex=r'^[0-9]+$')

titles = [('Ms', 'Miss'), ('Mrs', 'Missus'), ('Mr', 'Mister'), ('Master', 'Master'),
          ('Dr', 'Doctor'), ('Fr', 'Father'), ('Rev', 'Reverend'),
          ('Atty', 'Attorney'), ('Hon', 'Honorable'), ('Prof', 'Professor'),
          ('Pres', 'President'), ('Vp', 'Vice President'), ('Gov', 'Governor'),
          ('Ofc', 'Office'), ('other', 'other')]
# Create your models here.


class DollarInput(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            value = '$' + str(value)
        return super().render(name, value, attrs, renderer)


class DollarField(models.DecimalField):
    def fromfield(self, **kwargs):
        kwargs['widget'] = DollarInput
        return super().formfield(**kwargs)


class CreditCardExpirationField(models.Model):
    expiration_month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)], default=datetime.date.today().month)
    expiration_year = models.IntegerField(
        validators=[MinValueValidator(1)], default=(datetime.date.today().year))

    def __str__(self) -> str:
        return f'{self.expiration_month}/{self.expiration_year}'


class ModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DecimalField: {'widget': DollarInput},
    }

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields if isinstance(field, DollarField)]

    # def price_display(self, obj):
    #     return '$' + str(obj.price)
    # price_display.short_description = 'Price'


class Customer(models.Model):
    customer_id = models.BigAutoField(
        primary_key=True, unique=True, editable=False)
    company_name = models.CharField(max_length=200)
    contact_first_name = models.CharField(max_length=50)
    contact_last_name = models.CharField(max_length=50)
    billing_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5, validators=[postal_validator])
    country = models.CharField(max_length=50)
    contact_title = models.CharField(
        max_length=100, choices=titles, default='other')
    phone_number = models.CharField(max_length=20)
    mobile_phone_number = models.CharField(max_length=20)
    fax_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, unique=True)
    notes = models.TextField()

    def __str__(self) -> str:
        return str(self.contact_first_name + self.contact_last_name)


class Boat(models.Model):
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    mooring_no = models.CharField(max_length=100)
    mooring_location = models.CharField(max_length=200)
    depth = models.IntegerField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    last_check = models.DateField()
    boat_image = models.ImageField(upload_to='images/', default='',)

    def __str__(self) -> str:
        return str(self.name)

    def img_preview(self):
        """
        The img_preview function is a method that returns an image tag with the source set to the url of the boat_image field.
        The width of this image is set to 300 pixels.

        :param self: Refer to the current instance of the class
        :return: A mark_safe object that contains the html code for an image tag
        :doc-author: Davidag
        """

        return mark_safe('<img src = "{url}" width="300"/>'.format(url=self.boat_image.url))


class Employee(models.Model):
    employee_id = models.BigAutoField(
        primary_key=True, unique=True, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    extension = models.CharField(max_length=50)
    work_phone = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.first_name + self.last_name


class Shipping_Method(models.Model):
    shipping_method_id = models.BigAutoField(primary_key=True, unique=True)
    shipping_method = models.CharField(max_length=100)


class Order(models.Model):
    order_id = models.BigAutoField(
        primary_key=True, unique=True, editable=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    order_date = models.DateField()
    purchase_order_number = models.ForeignKey(
        Boat, db_column='mooring_no', on_delete=models.CASCADE)
    ship_name = models.CharField(max_length=50)
    ship_address = models.CharField(max_length=200)
    ship_city = models.CharField(max_length=50)
    ship_state_or_province = models.CharField(max_length=50)
    ship_postal_code = models.CharField(
        max_length=5, validators=[postal_validator])
    ship_country = models.CharField(max_length=100)
    ship_phone_number = models.CharField(max_length=20)
    ship_date = models.DateField()
    shipping_method_id = models.ForeignKey(
        Shipping_Method, on_delete=models.CASCADE)
    freight_charge = DollarField(max_digits=10, decimal_places=2)
    sales_tax_rate = models.DecimalField(max_digits=10, decimal_places=10)
    notes = models.TextField()
    discount = models.IntegerField()
    mooring_id = models.CharField(
        max_length=200, validators=[number_validator])

    def __str__(self) -> str:
        return str(self.order_id) + str(self.order_date)


class Product(models.Model):
    product_id = models.BigAutoField(
        primary_key=True, unique=True, editable=False)
    product_name = models.CharField(max_length=100)
    unit_price = DollarField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return str(self.product_name)


class Order_Detail(models.Model):
    order_detail_id = models.BigAutoField(
        primary_key=True, unique=True, editable=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit_price = DollarField(max_digits=10, decimal_places=2)
    discount = models.IntegerField()

    def __str__(self) -> str:
        return str(self.order_detail_id)


class Payment_Method(models.Model):
    payment_method_id = models.BigAutoField(
        primary_key=True, unique=True, editable=False)
    payment_method = models.CharField(max_length=50)
    credit_card = models.BooleanField()

    def __str__(self) -> str:
        return str(self.payment_method)


class Payment(models.Model):
    payment_id = models.BigAutoField(
        primary_key=True, unique=True, editable=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_amount = DollarField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    credit_card_number = models.CharField(
        max_length=16, validators=[MinLengthValidator(15)])
    card_holders_name = models.CharField(max_length=50)
    credit_card_exp_date = CreditCardExpirationField()
    payment_method_id = models.ForeignKey(
        Payment_Method, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.payment_id)
