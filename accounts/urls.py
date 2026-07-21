from .views import Signup, Signin, SendOtp, ResetPassword
from django.urls import path
urlpatterns = [
    path("signup/", Signup.as_view(), name="signup"),
    path("signin/", Signin.as_view(), name="signin"),
    path("send-otp/", SendOtp.as_view(), name="send-otp"),
    path("reset-password/", ResetPassword.as_view(), name="reset-password"),
]
