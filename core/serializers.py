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
    site_user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('site_user',)
        
    def create(self, validated_data):
        """
        Overriding the default create method of serializer.
        :param validated_data: data containing all the details of Profile
        :return: returns Profile record
        """
        user_data = validated_data.pop('site_user')
        # fittings_data = validated_data.pop('fittings',)
        site_user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile, _ = Profile.objects.update_or_create(site_user=site_user)

        return profile

class FittingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Fittings serializer to return data from each bra fitting session
    """
    fitting_user = UserSerializer(required=True)
    # breakpoint()
    class Meta:
        model = BraFitting
        fields = (
        'fitting_user',
        'bra_size',
        'band_measurement',
        'band_size',
        'bust_measurement',
        'cup_size',
        'bust_circumference',
        'date_sized',
        'currently_wearing',
        )
    # breakpoint()
    def create(self, validated_data):
        """
        Overriding default create method of serializer.
        """
        user_data = validated_data.pop('fitting_user')
        # breakpoint()
        fitting_user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        fittings, _ = BraFitting.objects.update_or_create(
            fitting_user=fitting_user,
            bra_size=validated_data.pop('bra_size'),
            band_measurement=validated_data.pop('band_measurement'),
            band_size=validated_data.pop('band_size'),
            bust_measurement=validated_data.pop('bust_measurement'),
            cup_size=validated_data.pop('cup_size'),
            bust_circumference=validated_data.pop('bust_circumference'),
            date_sized=validated_data.pop('date_sized'),
            currently_wearing=validated_data.pop('bra_size'),
            )
        breakpoint()
        return fittings
