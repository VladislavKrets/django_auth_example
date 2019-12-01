from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from . import models

class RegisterUserSerializer(serializers.ModelSerializer):

    vk_id = serializers.IntegerField(source='username')
    code = serializers.CharField(source='password')
    is_admin = serializers.BooleanField(source='expandedUser.is_admin', required=False)

    class Meta:
        model = User
        fields = ('vk_id', 'code', 'is_admin')

    def create(self, validated_data):
        expanded_user_data = validated_data.pop('expandedUser', None)
        user = super(RegisterUserSerializer, self).create(validated_data)
        self.update_or_create_expanded_user(user, expanded_user_data)
        return user

    def update(self, instance, validated_data):
        expanded_user_data = validated_data.pop('expandedUser', None)
        self.update_or_create_expanded_user(instance, expanded_user_data)
        return super(RegisterUserSerializer, self).update(instance, validated_data)

    def update_or_create_expanded_user(self, user, expanded_user_data):
        models.ExpandedUser.objects.update_or_create(user=user, defaults=expanded_user_data)

class GetUserSerializer(serializers.ModelSerializer):
    vk_id = serializers.IntegerField(source='username')

    class Meta:
        model = User
        fields = ('id', 'vk_id')

class AddVKGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VKGroup
        fields = ('vk_id',)

class FullVKGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VKGroup
        fields = '__all__'


class FullVKHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Home
        fields = '__all__'

class FullVKFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flat
        fields = '__all__'

