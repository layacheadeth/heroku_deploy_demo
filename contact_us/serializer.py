from rest_framework import serializers
from .models import ContactUs

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContactUs
        fields=['listing_id','listing','name','email','phone','message','user_id','realtor_email']