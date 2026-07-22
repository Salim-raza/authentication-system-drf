from .serializers import UserSerializers, OtpCreateSerializers, ResetPasswordSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .utils import get_tokens_for_user
from .models import CustomUser, OTP
from rest_framework import status
from django.utils import timezone
import random

# Create your views here.
class Signup(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message" : "registrations successful", "data" : serializer.data}, status=status.HTTP_201_CREATED)
    
    
class Signin(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            email = serializer.validated_data["email"],
            password = serializer.validated_data["password"]
        )
        
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({"message": "Login Successfully .", "access_token" : token["access"], "refresh_token": token["refresh"]}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid Email OR Password."}, status=status.HTTP_401_UNAUTHORIZED)
    
class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"message": "Old Password is Incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        
        return Response({"message": "Password Changed Successfully."}, status=status.HTTP_200_OK)

    
class SendOtp(APIView):
        permission_classes = [AllowAny]
        
        def post(self, request, format=None):
            serializer = OtpCreateSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data["email"]
            
            if CustomUser.objects.filter(email=email).exists:
                user = CustomUser.objects.get(email=email)
                otp = random.randint(11111, 99999)
                
                OTP.objects.update_or_create(user=user, defaults={'otp': otp, 'create_at': timezone.now()})
                
                return Response({
                    "status": "success",
                    "message": "OTP Send Successfully to Your Gmail",
                }, status=status.HTTP_201_CREATED)
        
            return Response({
                "status": "failed",
                "message": "email doesnot exists",
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
class ResetPassword(APIView):
    
    def post(self, request, format=None):
        serializer = ResetPasswordSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]
        
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            
            if OTP.objects.filter(user=user, otp=otp).exists():
                user.set_password(new_password)
                user.save()
                
                return Response({
                    "status": "success",
                    "message": "Password Reset Successfully",
                }, status=status.HTTP_200_OK)
            
            return Response({
                "status": "failed",
                "message": "Invalid OTP",
            }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            "status": "failed",
            "message": "email doesnot exists",
        }, status=status.HTTP_400_BAD_REQUEST)
        
        