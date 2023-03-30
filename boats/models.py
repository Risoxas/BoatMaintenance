from django.db import models

# Create your models here.


class Boats(models.Model):
    type = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    mooring_no = models.IntegerField()
    mooring_location = models.CharField(max_length=200)
    depth = models.IntegerField()
    # customer_id = models.ForeignKey()
    last_check = models.DateTimeField()
