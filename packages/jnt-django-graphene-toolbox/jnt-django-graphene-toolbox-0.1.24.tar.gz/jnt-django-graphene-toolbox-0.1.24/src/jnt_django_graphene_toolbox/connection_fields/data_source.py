from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.settings import graphene_settings

from jnt_django_graphene_toolbox.connection_fields.mixins import (
    AuthMixin,
    OffsetPaginationMixin,
)
from jnt_django_graphene_toolbox.filters.mixins import ValidateFilterSetMixin
from jnt_django_graphene_toolbox.security.permissions import AllowAuthenticated

MAX_SIZE = graphene_settings.RELAY_CONNECTION_MAX_LIMIT


class DataSourceConnectionField(  # noqa: WPS215
    AuthMixin,
    OffsetPaginationMixin,
    ValidateFilterSetMixin,
    DjangoFilterConnectionField,
):
    """Data source connection field."""

    permission_classes = (AllowAuthenticated,)

    def __init__(self, model_type, fields=None, *args, **kwargs):
        """Initialize self."""
        if fields is None:
            fields = "__all__"
        super().__init__(model_type, fields, *args, **kwargs)
