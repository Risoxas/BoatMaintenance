from django.db import models

# Create your models here.


class Boats(models.Model):
    type = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    mooring_no = models.CharField(max_length=200)
    mooring_location = models.CharField(max_length=200)
    depth = models.IntegerField()
    # customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    last_check = models.DateField()
    image = models.ImageField(upload_to='images', null=True)

# class Customer(models.Model):
#     boat = models.ForeignKey(Boats)
