from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class userserilizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
        # exclude = ['otp']