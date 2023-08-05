from .fields import SelfHrefField
from rest_framework import serializers
from typing import Union, Iterable, Optional


class HrefModelSerializer(serializers.HyperlinkedModelSerializer):
    url_field_name = "self"
    serializer_url_field = SelfHrefField

    class Meta:
        fields: Union[str, Iterable]
        serializer_class: serializers.Serializer
        self_view: Optional[str] = None


__all__ = ["HrefModelSerializer"]
