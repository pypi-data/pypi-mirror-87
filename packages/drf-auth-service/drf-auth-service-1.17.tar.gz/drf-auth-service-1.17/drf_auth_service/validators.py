from datetime import timedelta

from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from drf_auth_service.models import ActivationCode


def validate_token_by_type(token, code_type):
    password_reset_token_validation_time = 24

    reset_password_token = get_object_or_404(ActivationCode, key=token, key_type=code_type)

    expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

    if timezone.now() > expiry_date:
        reset_password_token.delete()
        raise ValidationError(dict(detail='Token expired'))

    return reset_password_token
