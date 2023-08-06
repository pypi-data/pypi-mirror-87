from rest_framework import serializers
from rest_framework.fields import empty


class CharField(serializers.CharField):
    """Wrapper base serializer char field."""

    def __init__(self, **kwargs):
        """Init field, add password validator."""
        kwargs.setdefault("allow_null", True)
        kwargs.setdefault("allow_blank", True)
        super().__init__(**kwargs)

    def run_validation(self, data=empty):  # noqa: WPS110
        """Run data-validation."""
        validation = super().run_validation(data=data)

        if all((validation is None, self.allow_null, self.allow_blank)):
            validation = ""

        return validation
