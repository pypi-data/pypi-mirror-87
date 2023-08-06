from django.contrib.postgres.forms import SimpleArrayField
from django.forms import CharField
from django_filters import Filter


class StringsArrayField(SimpleArrayField):
    """StringsArrayField handles for postgres ArrayField."""

    def __init__(self, **kwargs):
        """Inits ArrayField with a base of StringField."""
        super().__init__(base_field=CharField(), **kwargs)


class StringsArrayFilter(Filter):
    """Filter which receives an array of strings."""

    field_class = StringsArrayField
