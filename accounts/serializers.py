from rest_framework import serializers
from .models import CustomUser



class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["name", "email", "password", "phone"]
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {
            "password": {"write_only": True}
        }
        
        def create(self, validated_data):
            return CustomUser.objects.create_user(
                name=validated_data["name"],
                email=validated_data["email"],
                password=validated_data["password"],
                phone=validated_data["phone"]
            )
class OtpCreateSerializers(serializers.Serializer):
    email = serializers.EmailField()