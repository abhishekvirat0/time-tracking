import jwt
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.userProfile.models import UserProfile
from apps.userProfile.serializers import UserSerializer, LoginSerializer
from rest_framework import status


class SignUpView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            if user:
                UserProfile.objects.create(user=user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY, algorithm="HS256")

            serializer = UserSerializer(user)

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

            # SEND RESPONSE
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class MyAccountView(GenericAPIView):

    def get(self, request):
        teams = request.user.teams.exclude(pk=request.user.userProfile.active_team_id)
        data = list(teams.values())
        return Response({'teams': data}, status=status.HTTP_200_OK)