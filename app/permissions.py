from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden


def is_authenticated_user(func):
    def test_token(request):
        token = request.data.get("token")
        if token:
            user_object = get_object_or_404(Token, key=token).user
            return func(request, user_object)
        else:
            return HttpResponseForbidden()

    return test_token
