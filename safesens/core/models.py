from django.db import models

from typing import Any

from django_countries.fields import CountryField
from django.contrib.postgres.fields import JSONField

from .utils.json_serializer import CustomJsonEncoder

class Address(models.Model):
    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    suburb = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=5, blank=True)
    country = CountryField()

    class Meta:
        ordering = ("pk",)

    @property
    def full_name(self):
        return "%s %s" % (self.street_address_1, self.street_address_2)

    def __str__(self):
        if self.street_address_2:
            return "%s - %s" % (self.street_address_1, self.street_address_2)
        return self.street_address_1

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False
        return self.as_data() == other.as_data()

    __hash__ = models.Model.__hash__

    def as_data(self):
        """Return the address as a dict suitable for passing as kwargs.

        Result does not contain the primary key or an associated user.
        """
        data = model_to_dict(self, exclude=["id", "user"])
        if isinstance(data["country"], Country):
            data["country"] = data["country"].code
        return data


class ModelWithMetadata(models.Model):
    private_metadata = JSONField(
        blank=True, null=True, default=dict, encoder=CustomJsonEncoder
    )
    metadata = JSONField(blank=True, null=True, default=dict, encoder=CustomJsonEncoder)

    class Meta:
        abstract = True

    def get_value_from_private_metadata(self, key: str, default: Any = None) -> Any:
        return self.private_metadata.get(key, default)

    def store_value_in_private_metadata(self, items: dict):
        if not self.private_metadata:
            self.private_metadata = {}
        self.private_metadata.update(items)

    def clear_private_metadata(self):
        self.private_metadata = {}

    def delete_value_from_private_metadata(self, key: str):
        if key in self.private_metadata:
            del self.private_metadata[key]

    def get_value_from_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def store_value_in_metadata(self, items: dict):
        if not self.metadata:
            self.metadata = {}
        self.metadata.update(items)

    def clear_metadata(self):
        self.metadata = {}

    def delete_value_from_metadata(self, key: str):
        if key in self.metadata:
            del self.metadata[key]