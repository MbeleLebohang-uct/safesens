from django.db import models

from django_countries.fields import CountryField

class Address(models.Model):
    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    suburb = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=5, blank=True)
    country = CountryField()

    class Meta:
        ordering = ("pk",)
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

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
