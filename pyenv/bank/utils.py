import secrets
from rest_framework.exceptions import ValidationError
import uuid


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def create_random_string_id():
    return secrets.token_hex(10)


def validate_required_field(field, subject):
    if(field == False):
        raise ValidationError(
            {"Message": "Error 400, " + subject + " is required"})
    else:
        return field


def validate_float_field(field, subject):
    try:
        float_field = float(field)
    except Exception:
        raise ValidationError(
            {"Message": "Error 400, " + subject + " must be a number"})

    return float_field
