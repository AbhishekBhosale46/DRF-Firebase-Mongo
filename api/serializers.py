from rest_framework import serializers

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, max_length=100)
    email = serializers.CharField(required=True, error_messages={'required': 'Email and password are required'})
    password = serializers.CharField(required=True, error_messages={'required': 'Email and password are required', 'min_length': 'This password is too short. It must be atleast 8 characters'}, min_length=8)
    first_name = serializers.CharField(required=False, max_length=100)
    last_name = serializers.CharField(required=False, max_length=100)


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, max_length=100)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField(write_only=True, required=False, max_length=100)
    last_name = serializers.CharField(write_only=True, required=False, max_length=100)

    def get_full_name(self, obj):
        return f'{obj.first_name}-{obj.last_name}'

    