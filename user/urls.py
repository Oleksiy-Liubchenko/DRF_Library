from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import ManagingUser, CreateUserView, UsersListView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManagingUser.as_view(), name="my_user"),
    path("register/", CreateUserView.as_view(), name="register"),
    path("all_users/", UsersListView.as_view(), name="users"),
]

app_name = "user"
