from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken

def redirect_with_token(backend, user, response, *args, **kwargs):
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)
    redirect_url = f"/auth/social/jwt/?access={access}&refresh={refresh}"
    return redirect(redirect_url)