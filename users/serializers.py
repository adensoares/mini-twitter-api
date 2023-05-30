from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'full_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

