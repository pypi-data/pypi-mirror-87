from typing import Dict, Optional

from django.utils.translation import gettext_lazy as _

from jnt_django_graphene_toolbox.errors.base import BaseGraphQLError

ACCESS_DENIED = "ACCESS_DENIED"


class GraphQLPermissionDenied(BaseGraphQLError):
    """Permission denied error."""

    _default_message: str = _(
        "You do not have permission to perform this action",
    )
    _default_extensions: Optional[Dict[str, str]] = {
        "code": ACCESS_DENIED,
    }
