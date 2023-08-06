from rest_framework import serializers

from jnt_django_graphene_toolbox.serializers.validators import (
    PasswordValidator,
)


class PasswordField(serializers.CharField):
    """Wrapper around serializer password field."""

    def __init__(self, **kwargs):
        """Init field, add password validator."""
        super().__init__(**kwargs)
        self.validators.append(PasswordValidator())
