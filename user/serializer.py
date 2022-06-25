from typing import OrderedDict
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import get_user_model

import re

class UserSerializer(serializers.ModelSerializer):
    """
        User serializer for signup and update user's fields 
    """
    confirm_password = serializers.CharField(min_length=5, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'bio', 'avatar', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{5,}$"
        if attrs.get('password'):
            if re.search(regex, attrs['password']):
                if attrs['password'] == attrs['confirm_password']:
                    attrs.pop('confirm_password')
                    return attrs
                raise serializers.ValidationError('Passwords must be equal!')
            raise serializers.ValidationError('Minimum five characters, at least one uppercase letter, one lowercase letter, one number and one special character')
        return attrs

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def to_representation(self, instance):
        contents = super(UserSerializer, self).to_representation(instance)
        return OrderedDict([(key, contents[key]) for key in contents if contents[key] is not None])
        

class UserProfileManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'bio', 'avatar',)

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        return user

    
    def to_representation(self, instance):
        contents = super(UserProfileManagerSerializer, self).to_representation(instance)
        return OrderedDict([(key, contents[key]) for key in contents if contents[key] is not None])
        


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=5, write_only=True)
    new_password = serializers.CharField(min_length=5, write_only=True)
    confirm_new_password = serializers.CharField(min_length=5, write_only=True)

    class Meta(UserSerializer.Meta):
        model = get_user_model()
        fields = ('old_password', 'new_password', 'confirm_new_password')


    def validate(self, attrs):
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{5,}$"
        if self.context['request'].user.check_password(attrs['old_password']):
            if attrs.get('new_password'):
                if re.search(regex, attrs['new_password']):
                    if attrs['new_password'] == attrs['confirm_new_password']:
                        attrs.pop('confirm_new_password')
                        return attrs
                    raise serializers.ValidationError('Passwords must be equal!')
                raise serializers.ValidationError('Minimum five characters, at least one uppercase letter, one lowercase letter, one number and one special character')
            return attrs
        raise serializers.ValidationError("Password is Invalid")

    def update(self, instance, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['new_password'])            
        user.save()
        return user

    
