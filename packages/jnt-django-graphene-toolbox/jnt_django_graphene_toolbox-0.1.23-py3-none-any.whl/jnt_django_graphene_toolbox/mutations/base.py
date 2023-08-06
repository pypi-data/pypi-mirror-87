import graphene

from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied
from jnt_django_graphene_toolbox.security.mixins.mutation import AuthMutation
from jnt_django_graphene_toolbox.security.permissions import AllowAuthenticated


class BaseMutation(AuthMutation, graphene.Mutation):
    """A base class mutation."""

    class Meta:
        abstract = True

    permission_classes = (AllowAuthenticated,)

    @classmethod
    def mutate(cls, root, info, **kwargs):  # noqa: WPS110
        """Mutate."""
        cls.check_premissions(root, info, **kwargs)

        return cls.do_mutate(root, info, **kwargs)

    @classmethod
    def check_premissions(cls, root, info, **kwargs) -> None:  # noqa: WPS110
        """Check premissions."""
        if not cls.has_permission(root, info, **kwargs):
            raise GraphQLPermissionDenied()

    @classmethod
    def do_mutate(cls, root, info, **kwargs) -> None:  # noqa: WPS110
        """Method should be implemente in subclass."""
        raise NotImplementedError
