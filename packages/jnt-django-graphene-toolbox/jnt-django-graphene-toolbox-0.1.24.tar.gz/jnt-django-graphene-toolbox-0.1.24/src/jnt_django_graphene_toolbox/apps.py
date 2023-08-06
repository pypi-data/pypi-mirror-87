from django.apps import AppConfig as DjangoAppConfig
from graphql.execution import utils
from jnt_django_toolbox.helpers.modules import load_module_from_app

from jnt_django_graphene_toolbox.helpers.values import get_variable_values


class AppConfig(DjangoAppConfig):
    """Application entry config."""

    name = "jnt_django_graphene_toolbox"
    verbose_name = "Django graphene toolbox"

    def ready(self):
        """Run this code when Django starts."""
        super().ready()

        load_module_from_app(self, "fields")
        load_module_from_app(self, "converters.models")
        load_module_from_app(self, "converters.serializers")
        load_module_from_app(self, "converters.forms")

        self._monkey_patch()

    def _monkey_patch(self) -> None:
        utils.get_variable_values = get_variable_values  # type: ignore
