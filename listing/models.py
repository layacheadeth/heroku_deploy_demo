from django.db import models
from realtor.models import Realtor
from datetime import datetime

class Listing(models.Model):
    realtor=models.ForeignKey(Realtor,on_delete=models.DO_NOTHING)
    title=models.CharField(max_length=100)
    address=models.CharField(max_length=150)
    city=models.CharField(max_length=15)
    zipcode=models.CharField(max_length=10)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2,max_digits=9)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    sqft = models.IntegerField()
    photo_main = models.ImageField(upload_to='photos/%Y/%M/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%M/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%M/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%M/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title


# Create your models here.
