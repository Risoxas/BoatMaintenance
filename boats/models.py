from django.db import models
from django.utils.html import mark_safe
# from django.core.validators import RegexValidator, MinLengthValidator, MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from django import forms
from django.contrib import admin
from functools import partial
# import datetime

postal_validator = RegexValidator(
    regex=r'^\d{4}$', message='Postal code must be a 4 digit number', code='invalid_postal_code')

number_validator = RegexValidator(regex=r'^[0-9]+$')

titles = [('Ms', 'Miss'), ('Mrs', 'Missus'), ('Mr', 'Mister'), ('Master', 'Master'),
          ('Dr', 'Doctor'), ('Fr', 'Father'), ('Rev', 'Reverend'),
          ('Atty', 'Attorney'), ('Hon', 'Honorable'), ('Prof', 'Professor'),
          ('Pres', 'President'), ('Vp', 'Vice President'), ('Gov', 'Governor'),
          ('Ofc', 'Office'), ('other', 'other')]
# Create your models here.


def get_path(instance, filename, folder=''):
    if folder:
        return f'order/{instance.order_id}/{folder}/{filename}'
    else:
        return f'boats/{instance.id}/{filename}'


class DollarInput(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            value = '$' + str(value)
        return super().render(name, value, attrs, renderer)


class DollarField(models.DecimalField):
    def fromfield(self, **kwargs):
        kwargs['widget'] = DollarInput
        return super().formfield(**kwargs)


# class CreditCardExpirationField(models.Model):
#     expiration_month = models.IntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(12)], default=datetime.date.today().month)
#     expiration_year = models.IntegerField(
#         validators=[MinValueValidator(1)], default=(datetime.date.today().year))

#     def __str__(self) -> str:
#         return f'{self.expiration_month}/{self.expiration_year}'


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
    company_name = models.CharField(max_length=200, blank=True, null=True)
    contact_first_name = models.CharField(max_length=50)
    contact_last_name = models.CharField(max_length=50)
    billing_address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state_province = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=5, validators=[
                                   postal_validator], blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    contact_title = models.CharField(
        max_length=100, choices=titles, default='other', blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    mobile_phone_number = models.CharField(
        max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return str(self.contact_first_name + ' ' + self.contact_last_name)

    def get_name(self):
        return str(self.contact_first_name)


class BoatModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.mooring_no


class Boat(models.Model):
    type = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=100)
    mooring_no = models.CharField(max_length=100)
    mooring_location = models.CharField(max_length=200)
    depth = models.IntegerField(blank=True, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True)
    last_check = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    boat_image1 = models.ImageField(
        upload_to=get_path, default='', null=True, blank=True)
    boat_image2 = models.ImageField(
        upload_to=get_path, default='', null=True, blank=True)
    boat_image3 = models.ImageField(
        upload_to=get_path, default='', null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name + ' ' + self.mooring_location + ' ' + (self.customer.get_name() if self.customer else ''))

    def get_mooring(self):
        return str(self.mooring_no)

    def img_preview(self):
        """
        The img_preview function is a method that returns an image tag with the source set to the url of the boat_image field.
        The width of this image is set to 300 pixels.

        :param self: Refer to the current instance of the class
        :return: The image of the boat in a safe format
        :doc-author: Davidag
        """
        images = ''
        if self.boat_image1:
            images += f'<img src="{self.boat_image1.url}" width="300"/>'
        if self.boat_image2:
            images += f'<img src="{self.boat_image2.url}" width="300"/>'
        if self.boat_image3:
            images += f'<img src="{self.boat_image3.url}" width="300"/>'
        return mark_safe(images)


class Employee(models.Model):
    employee_id = models.BigAutoField(
        primary_key=True, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    work_phone = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class Order(models.Model):
    order_id = models.BigAutoField(
        primary_key=True, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    order_date = models.DateField()
    boat_info = models.ForeignKey(
        Boat, on_delete=models.CASCADE, blank=True, null=True, related_name='boat_info')
    service_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    previous_image1 = models.ImageField(
        upload_to=partial(get_path, folder='previous'), blank=True, null=True)
    previous_image2 = models.ImageField(
        upload_to=partial(get_path, folder='previous'), blank=True, null=True)
    previous_image3 = models.ImageField(
        upload_to=partial(get_path, folder='previous'), blank=True, null=True)
    after_image1 = models.ImageField(
        upload_to=partial(get_path, folder='previous'), blank=True, null=True)
    after_image2 = models.ImageField(
        upload_to=partial(get_path, folder='previous'), blank=True, null=True)
    after_image3 = models.ImageField(
        upload_to=partial(get_path, folder='previous'), blank=True, null=True)

    def __str__(self) -> str:
        return str(self.order_id) + ' ' + str(self.order_date)

    def img_preview(self):
        """
        The img_preview function is a method that returns an image tag with the source set to the url of the boat_image field.
        The width of this image is set to 300 pixels.

        :param self: Refer to the current instance of the class
        :return: The image of the boat in a safe format
        :doc-author: Davidag
        """

        pre_images = ''
        post_images = ''

        if self.previous_image1:
            pre_images += f'<img src="{self.previous_image1.url}" width="300"/>'

        if self.previous_image2:
            pre_images += f'<img src="{self.previous_image2.url}" width="300"/>'

        if self.previous_image3:
            pre_images += f'<img src="{self.previous_image3.url}" width="300"/>'

        if self.after_image1:
            post_images += f'<img src="{self.after_image1.url}" width="300"/>'

        if self.after_image2:
            post_images += f'<img src="{self.after_image2.url}" width="300"/>'

        if self.after_image3:
            post_images += f'<img src="{self.after_image3.url}" width="300"/>'

        html = '<div style="display:flex;flex-direction: flex-row;"><div style="margin: .25rem;display:flex; flex-direction: column;">' + pre_images + '</div><div style="margin: .25rem;display:flex; flex-direction: column;">' + \
            post_images + '</div></div>'
        return mark_safe(html)

    def mooring_no(self):
        boat = self.boat_info
        return f'{boat.mooring_no}'


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
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit_price = DollarField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return str(self.order_detail_id)


# class Payment_Method(models.Model):
#     payment_method_id = models.BigAutoField(
#         primary_key=True, unique=True, editable=False)
#     payment_method = models.CharField(max_length=100)
#     credit_card = models.BooleanField()

#     def __str__(self) -> str:
#         return str(self.payment_method)


# class Payment(models.Model):
#     payment_id = models.BigAutoField(
#         primary_key=True, unique=True, editable=False)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     payment_amount = DollarField(max_digits=10, decimal_places=2)
#     payment_date = models.DateField()
#     credit_card_number = models.CharField(
#         max_length=16, validators=[MinLengthValidator(15)])
#     card_holders_name = models.CharField(max_length=100)
#     credit_card_exp_date = CreditCardExpirationField()
#     payment_method = models.ForeignKey(
#         Payment_Method, on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return str(self.payment_id)
