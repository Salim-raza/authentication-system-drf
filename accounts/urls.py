from .views import Signup, Signin
from django.urls import path
urlpatterns = [
    path("signup/", Signup.as_view(), name="signup"),
    path("signin/", Signin.as_view(), name="signin"),
]
