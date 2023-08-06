from django.utils.translation import gettext_lazy as _

from jnt_django_graphene_toolbox.errors.base import BaseGraphQLError

AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"


class GraphQLAuthenticationFailed(BaseGraphQLError):
    """Authentication failed error."""

    _default_message = _("MSG_UNABLE_TO_LOGIN_WITH_PROVIDED_CREDENTIALS")
    _default_extensions = {
        "code": AUTHENTICATION_FAILED,
    }
