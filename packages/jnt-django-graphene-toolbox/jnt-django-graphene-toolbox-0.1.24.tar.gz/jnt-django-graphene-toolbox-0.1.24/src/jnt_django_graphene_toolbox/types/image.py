from typing import Optional

import graphene


class ImageType(graphene.Scalar):
    """
    Graphql type for images.

    We need show full url of image
    """

    @classmethod
    def coerce_path(cls, image_value) -> Optional[str]:
        """Extract url from image."""
        if not image_value:
            return ""

        return image_value.url

    @classmethod
    def serialize(cls, image_value):
        """Serialize."""
        return cls.coerce_path(image_value)

    @classmethod
    def parse_value(cls, image_value):
        """Parse value."""
        return cls.coerce_path(image_value)

    @classmethod
    def parse_literal(cls, ast):
        """Parse literal."""
        return ast.value
