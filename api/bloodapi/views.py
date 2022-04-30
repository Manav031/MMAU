from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Profile, BloodRequirement
from rest_framework.status import *
from .serializers import RegisterUserSerializer, ProfileSerializer, ProfileCreateSerializer, BloodRequirementSerializer, BloodSerializer, RewardPointSerializer
import json
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.

@api_view(["GET"])
def indexview(request):
    return Response({"message":"success"})

@api_view(["POST"])
def registerUser(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            user.save()
            token = Token.objects.get(user=user).key
            return Response({"data": serializer.data, "token":token}, status=HTTP_201_CREATED)
    return Response({"error": serializer.errors}, status=HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def userProfile(request):
    try:
        profile_data = Profile.objects.get(user=request.user.id)
    except:
        return Response({"error":"404 not found"}, status=HTTP_404_NOT_FOUND)

    serializer = ProfileSerializer(profile_data)
    return Response({"data": serializer.data})


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def userProfileCreate(request):
    try:
        profile_data = Profile.objects.get(user=request.user.id)
    except:
        return Response({"error": "404 not found"}, status=HTTP_404_NOT_FOUND)

    serializer = ProfileCreateSerializer(profile_data, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"success"}, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def createBloodRequest(request):
    serializer = BloodSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, name=request.user.profile.name, mobile_no=request.user.profile.mobile_no)
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def getBloodDetail(request):
    try:
        data_blood = BloodRequirement.objects.filter(user=request.user)
    except:
        return Response({"error":"404 not found"}, status=HTTP_404_NOT_FOUND)

    serializer = BloodRequirementSerializer(data_blood, many=True)
    return Response({"data":serializer.data})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def viewBloodDetail(request, id):
    try:
        data = BloodRequirement.objects.get(id=id)
    except:
        return Response({"error":"404 not found"})

    serializer = BloodSerializer(data)
    return Response({"data":serializer.data}, status=HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def editBloodDetail(request, id):
    try:
        data = BloodRequirement.objects.get(id=id)
    except:
        return Response({"error":"404 not found"})

    if request.user != data.user:
        return Response({"error":"not authorized"})
    serializer = BloodSerializer(data, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data":serializer.data}, status=HTTP_200_OK)
    return Response(status=HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteBloodDetail(request, id):
    try:
        data = BloodRequirement.objects.get(id=id)
    except:
        return Response({"error":"404 not found"})

    if request.user != data.user:
        return Response({"error":"not authorized"})
    data.delete()
    return Response({"message":"success"}, status=HTTP_202_ACCEPTED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def transferPoint(request, id):
    try:
        data = BloodRequirement.objects.get(id=id)
    except:
        return Response({"error":"404 not found"})

    reward = Profile.objects.get(user=request.user)
    receive = request.data['reward_point']
    if reward.reward_point >= int(receive):
        serializer1 = RewardPointSerializer(reward, data={"reward_point":(reward.reward_point-int(receive))})
        
        if serializer1.is_valid():
            serializer1.save()
            # print(serializer1.data['reward_point'])
            receiver_user = BloodRequirement.objects.get(id=id)
            recevier_profile = Profile.objects.get(user=receiver_user.user)
            rp = recevier_profile.reward_point
            if request.user == receiver_user.user:
                return Response({"error":"you can not transfer to yourself"})
                
            serializer2 = RewardPointSerializer(recevier_profile, data={"reward_point": (rp+int(receive))})
            if serializer2.is_valid():
                serializer2.save()
                print(request.user)
                print(recevier_profile.user)
                return Response({"sender_data":serializer1.data, "receiver_data":serializer2.data}, status=HTTP_201_CREATED)
        return Response({"error":"not valid"})
    return Response({"error":"not enough points"})