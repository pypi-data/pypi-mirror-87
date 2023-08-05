from urllib.parse import urlparse

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenViewBase

from drf_auth_service.authentication.serializers import LoginSerializer, EBSTokenRefreshSerializer, \
    ReturnRegisterSerializer, ReturnAccessTokenSerializer, ReturnJWTTokensSerializer
from drf_auth_service.common.backends import BaseBackend
from drf_auth_service.common.managers import BaseManager
from drf_auth_service.common.mixins import GenericEBSViewSet
from drf_auth_service.common.permissions import ServiceTokenPermission
from drf_auth_service.common.register_backends import RegisterManager
from drf_auth_service.models import ActivationCode
from drf_auth_service.settings import settings

jwt_response = openapi.Response('Respond with jwt access&refresh token', ReturnRegisterSerializer)
refresh_response = openapi.Response('Respond with jwt access token, ', ReturnAccessTokenSerializer)


class AuthenticationViewSet(GenericEBSViewSet):
    serializer_create_class = settings.SERIALIZERS.REGISTER_SERIALIZER
    serializer_class = settings.SERIALIZERS.REGISTER_RETURN_SERIALIZER
    permission_classes_by_action = settings.PERMISSIONS.AUTHENTICATION_PERMISSIONS

    @action(detail=False, methods=['POST'])
    def register(self, request, *args, **kwargs):
        api_settings.SIGNING_KEY = request.service.secret_token
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        register_manager = RegisterManager(register_type=serializer.validated_data['register_type'], request=request)
        response = register_manager.register()
        return Response(response)

    @action(detail=False, methods=['POST'], url_path='restore-request',
            serializer_class=settings.SERIALIZERS.RETURN_SUCCESS_SERIALIZER,
            serializer_create_class=settings.SERIALIZERS.SEND_RESET_PASSWORD_SERIALIZER)
    def send_reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        manager = BaseManager.load_manager(serializer.validated_data['user'], configs=None, request=request)
        manager.send_reset_password(serializer.validated_data['user'])
        return Response(self.get_serializer(dict(message='Reset password was sent successfully')).data)

    @action(detail=False, methods=['POST'], url_path='restore-confirm',
            serializer_class=ReturnJWTTokensSerializer,
            serializer_create_class=settings.SERIALIZERS.RESET_PASSWORD_CONFIRMATION_SERIALIZER)
    def reset_password_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']

        reset_password_token = serializer.validated_data['token']
        reset_password_token.user.set_password(password)
        reset_password_token.user.save()

        ActivationCode.make_user_active(reset_password_token.user)
        return Response(BaseBackend.get_jwt_response(reset_password_token.user))

    @swagger_auto_schema(method='GET', request_body=no_body, responses={})
    @action(detail=False, methods=['GET'])
    def logout(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            settings.COOKIE_KEY,
            "",  # Clean the token
            max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(),
            domain=urlparse(settings.DOMAIN_ADDRESS).netloc if settings.DOMAIN_ADDRESS else None,
            httponly=True,
            secure=True
        )
        response.cookies[settings.COOKIE_KEY]['samesite'] = 'None'
        return response


class LoginViewSet(TokenViewBase):
    serializer_class = LoginSerializer
    permission_classes = (ServiceTokenPermission,)

    @swagger_auto_schema(request_body=LoginSerializer, responses={200: jwt_response})
    def post(self, request, *args, **kwargs):
        api_settings.SIGNING_KEY = request.service.secret_token
        response = super(LoginViewSet, self).post(request, *args, **kwargs)
        response.set_cookie(
            settings.COOKIE_KEY,
            response.data['refresh'],
            max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(),
            domain=urlparse(settings.DOMAIN_ADDRESS).netloc if settings.DOMAIN_ADDRESS else None,
            httponly=True,
            secure=True
        )
        response.cookies[settings.COOKIE_KEY]['samesite'] = 'None'
        return response


class EBSTokenRefreshView(TokenViewBase):
    serializer_class = EBSTokenRefreshSerializer
    permission_classes = (ServiceTokenPermission,)

    @swagger_auto_schema(request_body=EBSTokenRefreshSerializer, responses={200: refresh_response})
    def post(self, request, *args, **kwargs):
        api_settings.SIGNING_KEY = request.service.secret_token
        return super().post(request, *args, **kwargs)
