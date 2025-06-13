from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    raise serializers.ValidationError("User is deactivated.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include both username and password.")

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRating
        fields = ['userId', 'movieId', 'rating', 'timestamp']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = '__all__'
    def get_ratings(self, obj):
        rating_obj = MovieRatings.objects.filter(movie=obj).first()
        return rating_obj.ratings if rating_obj else None


        
        