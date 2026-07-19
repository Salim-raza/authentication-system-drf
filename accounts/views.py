from rest_framework.permissions import AllowAny
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import UserSerializers
from rest_framework import status

# Create your views here.
class Signup(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message" : "registrations successful", "data" : serializer.data}, status=status.HTTP_201_CREATED)