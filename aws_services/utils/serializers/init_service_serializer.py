from rest_framework import serializers
from django.contrib.auth import get_user_model

from init_service.models import AWSUser, Role, UserScreens

User = get_user_model()


class UserScreensSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScreens
        fields = ["user_screen"]


class RoleSerializer(serializers.ModelSerializer):
    screens = UserScreensSerializer(required=True)

    class Meta:
        model = Role
        fields = ["role_name", "role_status", "screens"]

    def create(self, validated_data):
        screens = validated_data.pop("screens")
        user_screen = UserScreens.objects.create(**screens)
        role = Role.objects.create(screens=user_screen, **validated_data)

        return role


class CreateUserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        # Extract password data from validated_data if present
        password = validated_data.pop("password", None)

        user = User.objects.create(**validated_data)

        # If password is present, set it using Django's default set_password() method
        if password:
            user.set_password(password)
            user.save()

        return user


class AWSUserSerializer(serializers.ModelSerializer):
    # role = RoleSerializer()
    # user = CreateUserSerializer()

    class Meta:
        model = User
        # Define fields to include in serialization/deserialization
        fields = "__all__"

    # def create(self, validated_data):
    #     print("VALIDATED DATA ==>", validated_data)
    #     # Extract necessary data from validated_data as it needs to be created separately
    #     aws_user_data = validated_data.pop("aws_user")
    #     user_data = validated_data.pop("user")
    #     # role_data = user_data.pop("role_id")
    #
    #     role = Role.objects.create(**validated_data)
    #
    #     user = User.objects.create(**user_data)
    #
    #     # Create the AWSUser object with the profile data and the User object
    #     aws_user = AWSUser.objects.create(user=user, role_id=role, **aws_user_data)
    #     # Return the AWSUser object
    #     return aws_user
