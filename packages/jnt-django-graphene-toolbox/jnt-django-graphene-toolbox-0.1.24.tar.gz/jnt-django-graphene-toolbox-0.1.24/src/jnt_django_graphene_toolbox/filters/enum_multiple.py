from jnt_django_toolbox.forms.fields import MultipleEnumChoiceField

from jnt_django_graphene_toolbox.filters.strings_array import (
    StringsArrayFilter,
)


class EnumMultipleFilter(StringsArrayFilter):
    """Enum multiple filter."""

    field_class = MultipleEnumChoiceField

    def __init__(self, *args, **kwargs) -> None:
        """Init enum multiple filter."""
        kwargs.setdefault("lookup_expr", "in")
        super().__init__(*args, **kwargs)
