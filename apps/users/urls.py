from django.urls import path, include
from apps.users.views import RegisterView, LogoutView
from apps.users.views import (
    SocialJWTCallbackView,
    RegisterView,
    LoginView,
    CustomTokenRefreshView,
    LogoutView,
    SocialAuthInfoView,
    UserAdminCreateView
)

urlpatterns = [
    path("auth/social/", include("social_django.urls", namespace="social")),
    path("auth/social/jwt/", SocialJWTCallbackView.as_view(), name="social_jwt_callback"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/social/info/", SocialAuthInfoView.as_view(), name="social_info"),
    path('admin/users/create/', UserAdminCreateView.as_view(), name='admin-create-user'),
]