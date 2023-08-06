from typing import Optional

import graphene
from graphql import ResolveInfo

from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied
from jnt_django_graphene_toolbox.security.mixins.mutation import AuthMutation
from jnt_django_graphene_toolbox.security.permissions import AllowAuthenticated


class NoInputMutation(AuthMutation, graphene.Mutation):
    """Base for non parametrized mutations."""

    class Meta:
        abstract = True

    permission_classes = (AllowAuthenticated,)

    @classmethod
    def mutate(
        cls, root: Optional[object], info: ResolveInfo,  # noqa: WPS110
    ):
        """Mutation handler."""
        cls.check_premissions(root, info)

        return cls.perform_mutate(root, info)

    @classmethod
    def check_premissions(
        cls, root: Optional[object], info: ResolveInfo,  # noqa: WPS110
    ) -> None:
        """Check permissions handler."""
        if not cls.has_permission(root, info):
            raise GraphQLPermissionDenied()

    @classmethod
    def perform_mutate(
        cls, root: Optional[object], info: ResolveInfo,  # noqa: WPS110
    ) -> "NoInputMutation":
        """Overrideable mutation handler."""
        raise NotImplementedError
