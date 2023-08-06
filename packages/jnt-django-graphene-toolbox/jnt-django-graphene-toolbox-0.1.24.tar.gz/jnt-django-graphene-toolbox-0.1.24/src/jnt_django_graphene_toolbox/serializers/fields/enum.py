from rest_framework import serializers


class EnumField(serializers.ChoiceField):
    """
    Wrapper around serializer choices field.

    For graphene enum types detecting and rigth building.
    """

    def __init__(self, enum, **kwargs):
        """Initializer."""
        self.enum = enum
        super().__init__(choices=enum.choices, **kwargs)
