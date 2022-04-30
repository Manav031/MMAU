from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, BloodRequirement
from rest_framework.validators import UniqueValidator

class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=200, validators=[UniqueValidator(User.objects.all())] )
    email = serializers.EmailField(required=True, validators=[UniqueValidator(User.objects.all())] )
    password = serializers.CharField(min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('user', )

class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        exclude = ('user', 'reward_point', 'blood_donated_counter', 'last_blood_donated')

class BloodRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequirement
        exclude = ['user']

class BloodSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username', read_only=True)
    name = serializers.ReadOnlyField(source='user.profile.name', read_only=True)
    mobile_no = serializers.ReadOnlyField(source='user.profile.mobile_no', read_only=True)

    class Meta:
        model = BloodRequirement
        fields = ['user', 'name', 'mobile_no', 'blood_group', 'units', 'location']

    # def create(self, validated_data):
    #     data = BloodRequirement.objects.create(user=self.user, name=self.name, mobile_no=self.mobile_no)
    #     return data

class RewardPointSerializer(serializers.ModelSerializer):
    reward_point = serializers.IntegerField()
    class Meta:
        model = Profile
        fields = ['reward_point']