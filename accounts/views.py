from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializers, OtpCreateSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .utils import get_tokens_for_user
from rest_framework import status
from .models import CustomUser

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
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
        )
        
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({"message": "Login Successfully .", "access_token" : token["access"], "refresh_token": token["refresh"]}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid Email OR Password."}, status=status.HTTP_401_UNAUTHORIZED)
    
    
# class SendOtp(APIView):
#         permission_classes = [AllowAny]
        
#         def post(self, request, format=None):
#             serializer = OtpCreateSerializers(data=request.data)
#             serializer.is_valid(raise_exception=True)
            
#             email = serializer.validated_data["email"]
            
#             if CustomUser.objects.filter(email=email).exists:
#                 email = 