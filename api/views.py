from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from .utils import get_user_by_name
import requests
import json
import os
from dotenv import load_dotenv
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from rest_framework.serializers import ValidationError
from .models import User
load_dotenv()


@api_view(['POST'])
def register(request):
    user_serializer = UserRegistrationSerializer(data=request.data)

    if user_serializer.is_valid(raise_exception=True):

        username = user_serializer.validated_data.get('username', '')
        email = user_serializer.validated_data.get('email')  
        password = user_serializer.validated_data.get('password')
        first_name = user_serializer.validated_data.get('first_name', '')
        last_name = user_serializer.validated_data.get('last_name', '')

        try:
            if(get_user_by_name(username)):
                raise ValidationError({'error': 'A user with that username already exists'})
            user = auth.create_user(email=email, password=password)
            user = auth.update_user(user.uid, display_name=username) 
            db_user = User(
                username = username,
                email = email,
                first_name = first_name,
                last_name = last_name
            )
            db_user.save()
            return Response({'username': user.display_name, 'email': user.email}, status=status.HTTP_201_CREATED)
        except auth.EmailAlreadyExistsError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    
    email = request.data.get('email')
    password = request.data.get('password') 
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.getenv('FB_WEB_KEY')}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()
        id_token = data["idToken"]
        user_email = data["email"]
        username = data["displayName"]
        response_payload = {
            "username": username,
            "email": user_email,
            "token": id_token
        }
        return Response(response_payload, status=status.HTTP_200_OK)
    else:
        error_message = response.json().get("error", {}).get("error", "Unkown error")
        if error_message == "INVALID_LOGIN_CREDENTIALS":
            response_payload = {"error": "Invalid email or password"}
        else:
            response_payload = {"error": error_message}
        return Response(response_payload, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def profile_view(request):
    try:
        user_email = request.firebase_user['email']
        user = User.objects.get(email=user_email)
        user_serializer = UserProfileSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def profile_edit(request):
    user_profile_serializer = UserProfileSerializer(data=request.data)

    if user_profile_serializer.is_valid(raise_exception=True):
        
        new_username = user_profile_serializer.validated_data.get('username', '')
        new_first_name = user_profile_serializer.validated_data.get('first_name', '')
        new_last_name = user_profile_serializer.validated_data.get('last_name', '')

        user_email = request.firebase_user['email']

        try: 
            old_user_profile = User.objects.get(email=user_email)

            if new_username:
                if(get_user_by_name(new_username)):
                    raise ValidationError({'error': 'A user with that username already exists'})
                else :
                    old_user_profile.username = new_username

            if new_first_name:
                old_user_profile.first_name = new_first_name

            if new_last_name:
                old_user_profile.last_name = new_last_name

            old_user_profile.save()

            user_profile_serializer = UserProfileSerializer(old_user_profile)

            return Response(user_profile_serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)