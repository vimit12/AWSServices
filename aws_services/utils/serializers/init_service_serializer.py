from rest_framework import serializers
from django.contrib.auth import get_user_model

from ...init_service.models import AWSUser, Role, UserScreens

User = get_user_model()


class ConnectMeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AWSUser
        fields = ["id", "mobile"]


# Define a serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    # Use the ConnectMeUserSerializer to serialize/deserialize the profile field
    profile = ConnectMeUserSerializer(required=True)

    class Meta:
        model = User
        # Define fields to include in serialization/deserialization
        fields = ["username", "email", "password", "first_name", "last_name", "profile"]

    def create(self, validated_data):
        # Extract profile data from validated_data as it needs to be created separately
        profile_data = validated_data.pop("profile")
        # Extract password data from validated_data if present
        password = validated_data.pop("password", None)
        # Create the User object with the remaining validated_data
        user = User.objects.create(**validated_data)
        # If password is present, set it using Django's default set_password() method
        if password:
            user.set_password(password)
            user.save()
        # Create the ConnectMeUser object with the profile data and the User object
        connect_user = ConnectMeUser.objects.create(user=user, **profile_data)
        # Return the connect_user object
        return connect_user


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "full_name"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class GetUserListSerializer(serializers.ModelSerializer):
    # user = UserProfileSerializer()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = ConnectMeUser
        fields = ["id", "login_status", "full_name"]

    def get_full_name(self, obj):
        return obj.user.get_full_name()
