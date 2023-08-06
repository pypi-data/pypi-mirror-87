from django.contrib.postgres.forms import SimpleArrayField
from django.forms import IntegerField
from django_filters import Filter


class IntegersArrayField(SimpleArrayField):
    """IntegersArrayField handles for postgres ArrayField."""

    def __init__(self, **kwargs):
        """Inits ArrayField with a base of IntegerField."""
        super().__init__(base_field=IntegerField(), **kwargs)


class IntegersArrayFilter(Filter):
    """Filter which receives an array of integers."""

    field_class = IntegersArrayField
