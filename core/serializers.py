from django.contrib.auth.models import User, Group
from .models import Profile, BraFitting, Suggestion
from rest_framework import serializers, status

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
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

class FittingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Fittings serializer to return data from each bra fitting session
    """
    class Meta:
        model = BraFitting
        fields = ('user', 'bra_size', 'band_measurement', 'band_size', 'bust_measurement', 'cup_size', 'bust_circumference', 'date_sized', 'currently_wearing')
