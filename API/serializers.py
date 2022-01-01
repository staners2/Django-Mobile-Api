from rest_framework import serializers
from .models import UserProfile, Error, Countries, Histories, Types, Fact

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        depth = 1
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        depth = 1
        fields = "__all__"