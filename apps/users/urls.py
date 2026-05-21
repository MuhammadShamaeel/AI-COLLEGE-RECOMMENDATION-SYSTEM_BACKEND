from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from .views import (
    RegisterView,
    CustomLoginView,
    UserProfileView
)

urlpatterns = [

    # Register
    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    # Login
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login"
    ),

    # Refresh Token
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    # User Profile
    path(
        "profile/",
        UserProfileView.as_view(),
        name="profile"
    ),
]