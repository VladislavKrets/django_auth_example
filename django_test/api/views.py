from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import status

from . import models
from . import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class registerHome(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        # token get or none
        token = Token.objects.get(key=token)
        user = token.user
        if user.expandeduser.is_admin:
            serialized = serializers.AddVKHomeSerializer(data=request.data)
            if serialized.is_valid():

                serialized.validated_data['user_id'] = user
                group = serialized.save()
                serialized = serializers.FullVKHomeSerializer(group)
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status.HTTP_403_FORBIDDEN)


# register group
class registerGroup(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        # token get or none
        token = Token.objects.get(key=token)
        user = token.user
        serialized = serializers.AddVKGroupSerializer(data=request.data)

        if serialized.is_valid():
            group = models.VKGroup.objects.filter(vk_id=serialized.validated_data['vk_id'])
            if not group:
                group = models.VKGroup.objects.get_or_create(user_id=user, vk_id=serialized.validated_data['vk_id'])
                user.expandeduser.is_admin = True
                user.expandeduser.save()
                return Response(serialized.validated_data, status=status.HTTP_201_CREATED)
            else:
                return Response(status = status.HTTP_400_FORBIDDEN)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


# get user
class getUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        # token get or none
        token = Token.objects.get(key=token)
        user = token.user
        serialized = serializers.GetUserSerializer(user)
        return Response(serialized.data)


@api_view(['POST'])
def register(request):
    serialized = serializers.RegisterUserSerializer(data=request.data)
    if serialized.is_valid():
        user = serialized.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def auth(request):
    serialized = serializers.RegisterUserSerializer(data=request.data)
    if serialized.is_valid():
        # user get or none
        user = User.objects.get(username=serialized.validated_data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
