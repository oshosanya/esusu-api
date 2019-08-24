from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SavingsGroup, SavingsGroupMember, SavingsGroupInvite
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=32)
    first_name = serializers.CharField(required=True, max_length=32)
    last_name = serializers.CharField(required=True, max_length=32)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=6)

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]
        read_only_fields = ['pk']


class SavingsGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=64)

    class Meta:
        model = SavingsGroup
        fields = [
            'pk',
            'name'
        ]
        read_only_fields = ['pk']


class SavingsGroupInviteSerializer(serializers.ModelSerializer):
    savings_group = serializers.PrimaryKeyRelatedField(queryset=SavingsGroup.objects.all())
    invitee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SavingsGroupInvite
        fields = [
            'savings_group',
            'invitee'
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=SavingsGroupInvite.objects.all(),
                fields=['savings_group', 'invitee']
            )
        ]

    def create(self, validated_data):
        return SavingsGroupInvite.objects.create(**validated_data)


class SavingsGroupMemberSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SavingsGroupMember
        fields = [
            'savings_group',
            'user',
            'amount_saved'
        ]

    def create(self, validated_data):
        return SavingsGroupMember.objects.create(**validated_data)

