from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id', 'username', 'email', 'password']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    # create function runs after view accepts the data and before the data is entered to the model
    def create(self, validated_data):
        # getting the password from validataed request body
        password = validated_data.pop('password', None)

        # entering rest of the data to model
        instance = self.Meta.model(**validated_data)

        if password is not None:
            # setting hashed password
            instance.set_password(password)

        instance.save()

        return instance
