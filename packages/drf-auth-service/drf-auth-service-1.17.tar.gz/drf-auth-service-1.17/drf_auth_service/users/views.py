from drf_yasg import openapi
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings

from drf_auth_service.authentication.serializers import ReturnJWTTokensSerializer, ReturnSuccessSerializer
from drf_auth_service.common.backends import BaseBackend
from drf_auth_service.common.managers import BaseManager
from drf_auth_service.common.mixins import GenericEBSViewSet
from drf_auth_service.models import ActivationCode, UserBlock
from drf_auth_service.settings import User
from drf_auth_service.settings import settings

delete_user = openapi.Response('Endpoint to delete user by username', ReturnSuccessSerializer)


class UserViewSet(
    GenericEBSViewSet,
    mixins.DestroyModelMixin,
    ListModelMixin
):
    queryset = User.objects.all()
    serializer_class = settings.SERIALIZERS.USER_RETURN_SERIALIZER
    serializer_create_class = settings.SERIALIZERS.USER_SERIALIZER
    permission_classes_by_action = settings.PERMISSIONS.USER_PERMISSIONS
    lookup_field = 'username'
    lookup_value_regex = '[\w@.]+'

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer_create(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        model_obj = serializer.save()
        serializer_display = self.get_serializer(model_obj)
        return Response(serializer_display.data)

    def destroy(self, request, *args, **kwargs):
        super(UserViewSet, self).destroy(self, request, *args, **kwargs)
        return Response(dict(success=True, message=f"User was successfully deleted"))

    @action(detail=False, methods=['POST'], serializer_create_class=settings.SERIALIZERS.USER_CONFIRM_SERIALIZER,
            serializer_class=ReturnJWTTokensSerializer, url_path='confirm', url_name='confirm')
    def user_confirm(self, request, *args, **kwargs):
        api_settings.SIGNING_KEY = request.service.secret_token
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_password_token = serializer.validated_data['token']
        ActivationCode.make_user_active(reset_password_token.user)
        return Response(BaseBackend.get_jwt_response(reset_password_token.user))

    @action(detail=True, methods=['POST'], url_path='resend-confirmation',
            serializer_class=settings.SERIALIZERS.RETURN_SUCCESS_SERIALIZER,
            serializer_create_class=None)
    def resend_confirmation(self, request, *args, **kwargs):
        user = self.get_object()
        manager = BaseManager.load_manager(user, configs=None, request=request)
        manager.send_confirmation(user)
        return Response(self.get_serializer(dict(message='Confirmation was resent successfully')).data)

    @action(detail=True, methods=['POST'], url_path='block', url_name='block',
            serializer_class=settings.SERIALIZERS.RETURN_SUCCESS_SERIALIZER,
            serializer_create_class=settings.SERIALIZERS.BLOCK_USER_SERIALIZER)
    def block_user(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        UserBlock.objects.create(reason=serializer.validated_data['reason'], user=user)
        return Response(
            self.get_serializer(dict(message=f"User {user.username} was successfully blocked")).data
        )

    @action(detail=True, methods=['POST'], url_path='unblock', url_name='unblock',
            serializer_create_class=None,
            serializer_class=settings.SERIALIZERS.RETURN_SUCCESS_SERIALIZER)
    def unblock_user(self, request, *args, **kwargs):
        user = self.get_object()
        UserBlock.objects.get(user=user).delete()
        return Response(
            self.get_serializer(dict(message=f"User {user.username} was successfully unblocked")).data
        )

    @action(detail=True, methods=['POST'], serializer_create_class=settings.SERIALIZERS.SET_PASSWORD_SERIALIZER,
            serializer_class=settings.SERIALIZERS.RETURN_SUCCESS_SERIALIZER, url_path='set-password')
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(
            self.get_serializer(dict(message=f"Password for user {user.username} was successfully set")).data
        )

    def get_queryset(self):
        if getattr(self.request, 'service', None):
            return super().get_queryset().filter(service=self.request.service)
        return super().get_queryset()
