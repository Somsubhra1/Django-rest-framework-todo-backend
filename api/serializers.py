from django.db.models import fields
from rest_framework import serializers
from .models import Task

# Serializing the model for the API view


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task  # specify the model to serialize
        # Specify the field names to serialize
        # fields = ["id", "title"]

        # To serialize all field names use __all__
        fields = '__all__'
