from rest_framework import serializers
from .models import *


class CarSerializer(serializers.ModelSerializer):
    """
    Default serializer - featuring all datafields
    Not actually used in API
    """

    class Meta:
        model = Car
        fields = "__all__"


class CarSerializerPost(serializers.ModelSerializer):
    """
    Serializer for POST /cars/
    Requires only make and model of the car
    """

    class Meta:
        model = Car
        fields = ("make", "model")


class CarSerializerGet(serializers.ModelSerializer):
    """
    Serializer for GET /cars/
    Returns id, make, model and average rating
    """

    class Meta:
        model = Car
        fields = ("id", "make", "model", "avg_rating")


class CarSerializerDelete(serializers.ModelSerializer):
    """
    Serializer for DELETE /cars/{id}
    Requires only id for deletion
    """

    class Meta:
        model = Car
        fields = "id"


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for POST /rate/{id}
    Requires car_id and a rating
    """

    class Meta:
        model = Rating
        fields = ("car_id", "rating")


class PopularSerializer(serializers.ModelSerializer):
    """
    Serializer for GET /popular/
    Returns id, make, model and number of ratings
    """

    class Meta:
        model = Car
        fields = ("id", "make", "model", "rates_number")
