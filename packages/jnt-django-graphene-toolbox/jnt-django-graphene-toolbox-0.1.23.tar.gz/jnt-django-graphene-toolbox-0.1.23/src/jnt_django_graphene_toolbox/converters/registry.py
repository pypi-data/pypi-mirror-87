from graphene_django.registry import get_global_registry


def get_registered_enum(enum):
    """Get registered field for enum."""
    global_registry = get_global_registry()

    return next(
        (
            converted
            for converted in global_registry._field_registry.values()  # noqa:  WPS437
            if getattr(converted, "django_enum", None) == enum
        ),
        None,
    )
