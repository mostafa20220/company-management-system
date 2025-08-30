from users.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        try:
            django_validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def validate_refresh(self, value):
        try:
            token = RefreshToken(value)
            token.blacklist()  # Blacklist the refresh token
        except Exception as e:
            raise serializers.ValidationError("Invalid or expired refresh token.")

        return value

    def create(self, validated_data):
        return validated_data

class RetrieveProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'id' ,'email','username','role']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'id' ,'email','username','role']

class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username' ]

class RemoveUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    
    def validate(self, data):
        user = User.objects.filter(email=data.get('email'),id=data.get("id")).first()
        if not user:
            raise serializers.ValidationError("User with this email and id does not exist.")
        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data.get('user')
        user.is_active = False
        user.save()
        return user

