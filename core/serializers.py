from django.contrib.auth.models import User, Group
from .models import Profile
from rest_framework import serializers, status

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile Serializer to return all user and profile data
    """
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('user')
        
    def create(self, validated_data):
        """
        Overriding the default create method of serializer.
        :param validated_data: data containing all the details of Profile
        :return: returns Profile record
        """
        user_data = validated_data.pop('user', 'fittings')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile, created = Profile.objects.update_or_create(user=user, fittings=validated_data.pop('fittings'))

        return profile
