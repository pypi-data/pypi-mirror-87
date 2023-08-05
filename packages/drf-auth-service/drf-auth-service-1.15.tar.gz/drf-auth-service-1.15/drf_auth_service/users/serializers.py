from rest_framework import serializers

from drf_auth_service.models import ActivationCode
from drf_auth_service.services.serializers import ServiceSerializer
from drf_auth_service.settings import User
from drf_auth_service.socials.serializers import SocialModelSerializer
from drf_auth_service.validators import validate_token_by_type


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class ReturnUserBaseSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    user_social_identifier = SocialModelSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'service', 'is_blocked', 'user_social_identifier', 'is_confirmed')


class UserConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, allow_null=False, allow_blank=False,
                                  label="Token to confirm user")

    def validate_token(self, token):
        return validate_token_by_type(token, ActivationCode.CodeTypes.CONFIRM_ACCOUNT)


class UserIdentifierSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)


class UserSetPasswordSerializer(UserIdentifierSerializer):
    password = serializers.CharField(label="Password", required=True, allow_null=False, allow_blank=False)
    confirm_password = serializers.CharField(label="Confirm password", required=True,
                                             allow_null=False, allow_blank=False)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords does not match")

        return data


class BockUserSerializer(UserIdentifierSerializer):
    reason = serializers.CharField(required=True)
