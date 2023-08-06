from django.core.validators import URLValidator

from jnt_django_graphene_toolbox.serializers.fields.char import CharField


class URLField(CharField):
    """Wrapper around serializer email field."""

    def __init__(self, **kwargs):
        """Init field, add email validator."""
        super().__init__(**kwargs)
        self.validators.append(URLValidator())
