import uuid

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import Storage
from django.core.validators import RegexValidator
from django.db import models

from utils.models.abstract_model import CommonItems
from django.utils.deconstruct import deconstructible

User = get_user_model()


@deconstructible
class MinioStorage(Storage):
    def get_available_name(self, name, max_length=None):
        return name

    def _save(self, name, content):
        # Generate the new filename with <pk>.jpg or <pk>.png format
        extension = "jpg" if content.content_type == "image/jpeg" else "png"
        new_name = f"{self.model.profile.id}.{extension}"

        # Save the file to MinIO with the new filename
        self._save_content(new_name, content)

        return new_name


class Role(CommonItems):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("cloud basic", "Cloud Basic"),
        ("cloud manager", "Cloud Manager"),
        ("cloud expert", "Cloud Expert"),
        ("others", "Others"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(
        max_length=255, blank=True, null=True, choices=ROLE_CHOICES
    )
    role_status = models.BooleanField(default=True)
    screens = models.OneToOneField(
        "UserScreens", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"Role : {self.id}, Role Name : {self.role_name}"


class ProfilePicture(models.Model):
    profile = models.ForeignKey("AWSUser", on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        storage=MinioStorage(), upload_to="", default="default_profile_pic.jpg"
    )

    # Add any other fields for the profile picture here
    def __str__(self):
        return f"{self.profile.user.username} Profile Picture"

    @property
    def file_url(self):
        return self.profile_picture.url


class AWSUser(CommonItems):
    """
    AWS User model will inherit CommonItems and will have user model as one to one field.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_regex = RegexValidator(
        regex=r"^\+?\d{9,15}$",
        message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    mobile = models.CharField(validators=[mobile_regex], max_length=17, blank=True)
    login_status = models.BooleanField(default=False)

    role_id = models.ForeignKey("Role", on_delete=models.CASCADE, blank=True, null=True)
    access_token = models.JSONField(blank=True, null=True)
    refresh_token = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "aws_user"
        verbose_name = "AWS User"
        verbose_name_plural = "AWS Users"

    def __str__(self):
        return f"ID : {self.id}, User : {self.user.first_name} {self.user.last_name}"

    @property
    def _get_detail(self):
        _detail = {
            "id": str(self.id),
            "username": self.user.username,
            "name": self.user.first_name + " " + self.user.last_name
            if self.user.last_name
            else self.user.first_name,
            "email": self.user.email,
            "mobile": self.mobile,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "last_login": self.user.last_login,
            "login_status": self.login_status,
            "role": {
                "id": str(self.role_id.id),
                "role_name": self.role_id.role_name,
                "role_status": self.role_id.role_status,
            }
            if self.role_id
            else {},
            "user_screens": {
                "id": str(self.role_id.screens.id),
                "user_screen": self.role_id.screens.user_screen,
            }
            if self.role_id
            else {},
        }
        return _detail


class AvailableScreens(CommonItems):
    """
    Available Screens model will inherit CommonItems and will contains all the available servicce and screens.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    screen_json = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "available_screens"
        verbose_name = "Available Screen"
        verbose_name_plural = "Available Screens"

    def __str__(self):
        return f"ID : {self.id}"


class UserScreens(CommonItems):
    """
    User Screens model will inherit CommonItems and will contains all the screens corresponding to user.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_screen = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "user_screens"
        verbose_name = "User Screen"
        verbose_name_plural = "User Screens"

    def __str__(self):
        return f"ID : {self.id}"
