from django.db import models
from django.utils.html import mark_safe

# Create your models here.


class Boats(models.Model):

    type = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    mooring_no = models.CharField(max_length=200)
    mooring_location = models.CharField(max_length=200)
    depth = models.IntegerField()
    # customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    last_check = models.DateField()
    boat_image = models.ImageField(upload_to='images/', default='',)

    def img_preview(self):
        return mark_safe('<img src = "{url}" width="300"/>'.format(url=self.boat_image.url))
