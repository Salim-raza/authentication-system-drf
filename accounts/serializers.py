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