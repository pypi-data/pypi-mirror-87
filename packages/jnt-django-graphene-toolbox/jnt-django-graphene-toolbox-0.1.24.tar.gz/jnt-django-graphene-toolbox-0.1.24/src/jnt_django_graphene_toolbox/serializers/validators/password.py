from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class PasswordValidator:
    """Password validator."""

    code = "invalid"

    def __call__(self, password):
        """Run password validation."""
        if not password:
            raise ValidationError("Password is empty", code=self.code)

        validate_password(password=password)
