import graphene

from jnt_django_graphene_toolbox.connection_fields.mixins import (
    OffsetPaginationMixin,
)


class OffsetPaginationConnectionField(
    OffsetPaginationMixin, graphene.ConnectionField,
):
    """Supports pagination via offset, first, last, before, after arguments."""
