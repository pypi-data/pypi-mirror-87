from typing import Optional

from graphql import ResolveInfo

from jnt_django_graphene_toolbox.security.permissions import AllowAuthenticated


class AuthMutation:
    """Permission mixin for ClientIdMutation."""

    permission_classes = (AllowAuthenticated,)

    @classmethod
    def has_permission(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> bool:
        """Check has permission."""
        return all(
            (
                perm().has_mutation_permission(root, info, **kwargs)
                for perm in cls.permission_classes
            ),
        )
