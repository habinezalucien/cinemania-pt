from django.urls import path
from .views import createAccount


urlpatterns = [
    path("signup/", createAccount.as_view(), name="signup"),
]