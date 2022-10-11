from dataclasses import fields
from .models import SandwichModel, SauceModel
from rest_framework import serializers


class SauceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SauceModel
        fields = "__all__"


class SandwichSerializer(serializers.ModelSerializer):
    sauces = SauceSerializer(many=True)

    class Meta:
        model = SandwichModel
        fields = "__all__"
