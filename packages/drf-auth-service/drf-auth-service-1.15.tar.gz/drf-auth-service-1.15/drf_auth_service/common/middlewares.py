from rest_framework.exceptions import PermissionDenied

from drf_auth_service.models import Service


class ServiceTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def get_token(request):
        return request.headers.get('Secret-Token', None)

    def __call__(self, request):
        if request.path != '/':
            token = self.get_token(request)

            if token is None:
                raise PermissionDenied("Secret-Token is missing")

            request.service = Service.objects.filter(secret_token=token).first()

            if not request.service:
                raise PermissionDenied("Invalid Secret-Token")

        return self.get_response(request)
