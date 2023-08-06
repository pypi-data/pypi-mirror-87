from jnt_django_graphene_toolbox.connection_fields import (
    DataSourceConnectionField,
)
from jnt_django_graphene_toolbox.security.permissions import AllowAny


class DataSourceAllowAnyConnectionField(DataSourceConnectionField):
    """Data source connection field for any users."""

    permission_classes = (AllowAny,)
