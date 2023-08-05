import re
from typing import Dict, Any, Optional

from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch
from drf_yasg import openapi
from rest_framework import serializers
from rest_framework.relations import Hyperlink


class SelfHrefField(serializers.HyperlinkedIdentityField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "Self",
            "read_only": True,
            "properties": {
                "href": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_URI,
                    example="http://example.com/resource/1/"
                )
            }
        }

    def _get_url_representation(self,
                                value: Any,
                                view_name: Optional[str] = None
                                ) -> Optional[str]:
        """ Copied from base with a few adjustments for Viewname detection """
        assert "request" in self.context, (
                "`%s` requires the request in the serializer"
                " context. Add `context={'request': request}` when instantiating "
                "the serializer." % self.__class__.__name__
        )

        request = self.context["request"]
        format_ = self.context.get("format", None)

        if format_ and self.format and self.format != format_:
            format_ = self.format

        try:
            reverse_view = view_name or self.view_name
            url = self.get_url(value, reverse_view, request, format_)
        except NoReverseMatch:
            msg = (
                "Could not resolve URL for hyperlinked relationship using "
                "view name '%s'. You may have failed to include the related "
                "model in your API, or incorrectly configured the "
                "`lookup_field` attribute on this field."
            )
            if value in ("", None):
                value_string = {"": "the empty string", None: "None"}[value]
                msg += (
                        " WARNING: The value of the field on the model instance "
                        "was %s, which may be why it didn't match any "
                        "entries in your URL conf." % value_string
                )
            raise ImproperlyConfigured(msg % self.view_name)

        if url is None:
            return None

        return Hyperlink(url, value)

    def to_representation(self, value) -> Dict[str, str]:
        # If provided, prefer the provided self_view Meta parameter
        # of the parent serializer class.
        # We need to prefer this over the default view_name as it is
        # always going to be present - the serializer class will generate
        # a nonsensical default for it
        if hasattr(self.parent, "Meta"):
            if v := getattr(self.parent.Meta, "self_view", False):
                self.view_name = v
        url = self._get_url_representation(
            value, self.view_name
        )
        return {"href": url}


class HexColorField(serializers.Field):
    """ Saves hex color-values of lengths 3 or 6 to int in the Database """
    default_error_messages = {
        "incorrect_format": "Incorrect hex color format."
    }

    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_STRING,
            "title": "Color",
            "example": "#ffffff"
        }

    def to_representation(self, value: int):
        # Simply convert our value back to a string and add a #
        return hex(value).replace("0x", "#")

    def to_internal_value(self, data):
        # Validate that it is either a 3 or 6 digit hex-code with a # in it
        if not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', data):
            self.fail("incorrect_format")

        # strip the #
        data = data[1:]

        # Expand 3-digit hex for consistency
        if len(data) == 3:
            data = "".join(c * 2 for c in data)

        # Save the integer representation in the database
        # we do this because it is less bytes than saving it as a string
        return int(data, 16)


__all__ = ["SelfHrefField", "HexColorField"]
