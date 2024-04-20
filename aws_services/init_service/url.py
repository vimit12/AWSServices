from django.urls import include, path

from .views import (
    GetAllUser,
    LoginAPI,
    LogoutAPI,
    SignUp,
    UpdateUserProfile,
    UserNameAPI,
    RefreshTokeAPI,
)

urlpatterns = [
    path("api/sign_up/", SignUp.as_view()),
    path("api/username/", UserNameAPI.as_view()),
    path("api/login/", LoginAPI.as_view()),
    path("api/logout/", LogoutAPI.as_view()),
    path("api/refresh/", RefreshTokeAPI.as_view()),
    path("api/user_list/", GetAllUser.as_view()),
    path("api/user_update/", UpdateUserProfile.as_view()),
]
