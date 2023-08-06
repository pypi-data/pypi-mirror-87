from typing import Iterable, Tuple

import graphene


def text_choices_factory_type(
    type_name: str, text_choices: Iterable[Tuple[str, str]],
) -> type:
    """Generate ObjectType class from TextChoices."""
    return type(
        type_name,
        (graphene.ObjectType,),
        {
            choice[0].lower(): graphene.Int(default_value=0)
            for choice in text_choices
        },
    )
