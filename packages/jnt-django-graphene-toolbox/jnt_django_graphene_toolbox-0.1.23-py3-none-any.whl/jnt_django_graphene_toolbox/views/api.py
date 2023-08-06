from graphene_django.views import GraphQLView
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.request import Request


class BaseApiGraphQLView(GraphQLView):
    """Api GraphQL View."""

    permission_classes = None
    authentication_classes = None

    @classmethod
    def as_view(cls, *args, **kwargs):
        """Main entry point for a request-response process."""
        view = super().as_view(*args, **kwargs)
        view = permission_classes(cls.permission_classes)(view)
        view = authentication_classes(cls.authentication_classes)(view)
        view = api_view(["GET", "POST"])(view)
        return view  # noqa: WPS331

    def parse_body(self, request):
        """Parse body."""
        if isinstance(request, Request):
            return request.data

        return super().parse_body(request)
