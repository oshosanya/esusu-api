# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import UserSerializer, SavingsGroupSerializer, SavingsGroupMemberSerializer, SavingsGroupInviteSerializer
from .models import SavingsGroup, SavingsGroupMember, SavingsGroupInvite
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import make_password


from django.shortcuts import render

# Create your views here.


User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=request.data.get("username"),
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            email=request.data.get("email"),
            password=make_password(request.POST.get("password"))
        )

        Token.objects.create(user=user)

        return Response(
            data={"message": "User {} created successfully.".format(user.username)},
            status=status.HTTP_400_BAD_REQUEST
        )


class SavingsGroupView(viewsets.ModelViewSet):

    queryset = SavingsGroup.objects.all()
    serializer_class = SavingsGroupSerializer

    def list(self, request, *args, **kwargs):
        search_keyword = request.GET.get("q")
        if search_keyword is not None:
            queryset = SavingsGroup.objects.filter(name__icontains=search_keyword)
        else:
            queryset = SavingsGroup.objects.all()
        serializer = SavingsGroupSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def invite(self, request, pk):
        try:
            user = User.objects.get(username__exact=request.data['invitee'])
        except ObjectDoesNotExist:
            return Response({"status": "error", "message": "Invitee is not a valid user"})
        data = {"savings_group": pk, "invitee": user.pk}
        serializer = SavingsGroupInviteSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"status": "success", "message": "Invitation sent successfully"})
        except ValidationError:
            return Response({"status": "error", "message": "Invitation has been sent to this user before"})


class SavingsGroupMemberView(viewsets.ModelViewSet):

    queryset = SavingsGroupMember.objects.all()
    serializer_class = SavingsGroupMember

    def list(self, request, *args, **kwargs):
        queryset = SavingsGroupMember.objects.filter(savings_group__exact=kwargs['savings_group'])
        serializer = SavingsGroupMemberSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # request_data = request.data
        # # print(request_data['user']
        # # return
        # user = get_object_or_404(User, pk=request_data['user'])
        # print(user.__dict__)
        # request_data['user'] = user['pk']
        serializer = SavingsGroupMemberSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer)
            serializer.save()
            return Response({"status": "success", "data": []})

