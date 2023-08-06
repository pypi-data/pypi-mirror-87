import functools

from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied


def authenticated_only(func):
    """Forbids unauthenticated requests."""

    @functools.wraps(func)
    def wrapper_decorator(parent, info, **kwargs):  # noqa: WPS110, WPS430
        if not info.context.user.is_authenticated:
            raise GraphQLPermissionDenied()
        return func(parent, info, **kwargs)

    return wrapper_decorator
