from .views import Signup, Signin, SendOtp, ResetPassword, ChangePassword
from django.urls import path
urlpatterns = [
    path("signup/", Signup.as_view(), name="signup"),
    path("signin/", Signin.as_view(), name="signin"),
    path("change-password/", ChangePassword.as_view(), name="change-password"),
    path("send-otp/", SendOtp.as_view(), name="send-otp"),
    path("reset-password/", ResetPassword.as_view(), name="reset-password")
]
