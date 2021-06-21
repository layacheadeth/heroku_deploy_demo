from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Listing
        fields='__all__'

# class ListingSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model=Listing
#         fields=['realtor','title','address','zipcode','description','price','list_date','photo_main']



