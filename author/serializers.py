from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from .models import AuthorProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class AuthorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, read_only=True)

    image = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
                                   required=False)

    def validate(self, data):
        if data.get('age') > 200 or data.get('age') < 0:
            raise serializers.ValidationError({"Error": "Your Age is incorrect."})

        if data.get('about') and len(data.get('about')) > 300:
            raise serializers.ValidationError({"Error": "The maximum character of about can be 300."})

        if data.get('image') and data['image'].size > 6000000:
            raise serializers.ValidationError({"Error": "Image size too big!"})

        return super().validate(data)

    class Meta:
        model = AuthorProfile
        fields = ['user', 'age', 'image', 'about']
