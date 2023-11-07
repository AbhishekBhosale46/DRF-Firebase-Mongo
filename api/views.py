from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from rest_framework.decorators import api_view
from .utils import get_user_by_name
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        if(get_user_by_name(username)):
            return Response({'error': 'A user with that username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = auth.create_user(email=email, password=password)
        user = auth.update_user(user.uid, display_name=username) 
        return Response({'username': user.display_name, 'email': user.email}, status=status.HTTP_201_CREATED)
    except auth.EmailAlreadyExistsError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
        error_message = response.json().get("error", {}).get("message", "Unkown error")
        response_payload = {"message": error_message}
        return Response(response_payload, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def verify_login(request):
    return Response({"message": "This is returned because the token is valid"})