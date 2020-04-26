from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from django.utils import timezone

from versatileimagefield.fields import VersatileImageField

from .utils import CustomerTypes
from ..core.permissions import AccountPermissions
from ..core.models import Address, ModelWithMetadata


class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, user_type=None, is_superuser=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        extra_fields.pop("username", None)

        if not user_type:
            raise Exception("Error: User type is required.")

        user = self.model(
            email=email, is_active=is_active, user_type=user_type, is_superuser=is_superuser, **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            raise Exception("Error: User password is required.")

        user.save()

        permissions = []

        if user_type == CustomerTypes.STAFF:
            permissions = [Permission.objects.get(codename=AccountPermissions.MANAGE_STAFF.codename)]
        elif user_type == CustomerTypes.CONTRACTOR:
            permissions = [Permission.objects.get(codename=AccountPermissions.IS_CONTRACTOR.codename)]
        elif user_type == CustomerTypes.CONTRACTOR_CUSTOMER:
            permissions = [Permission.objects.get(codename=AccountPermissions.IS_CONTRACTOR_CUSTOMER.codename)]
        elif user_type == CustomerTypes.TECHNICIAN:
            permissions = [Permission.objects.get(codename=AccountPermissions.IS_TECHNICIAN.codename)]

        permissions.append(Permission.objects.get(codename='manage_devices'))

        for permission in permissions:
            user.user_permissions.add(permission)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, user_type=CustomerTypes.STAFF, is_superuser=True, **extra_fields
        )

    def contractor_customers(self):
        is_contractor_customer = CustomerTypes.CONTRACTOR_CUSTOMER
        return self.get_queryset().filter(user_type=is_contractor_customer)

    def contractors(self):
        is_contractor = CustomerTypes.CONTRACTOR
        return self.get_queryset().filter(user_type=is_contractor)

    def technicians(self):
        is_technician = CustomerTypes.TECHNICIAN
        return self.get_queryset().filter(user_type=is_technician)

    def staff(self):
        is_staff = CustomerTypes.STAFF
        return self.get_queryset().filter(user_type=is_staff)


class User(PermissionsMixin, ModelWithMetadata, AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    user_type = models.IntegerField(choices=CustomerTypes.choices(), null=False, blank=False) 
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    home_device_imei = models.CharField("Home device imei", max_length=50, default="", blank=True)
    avatar = VersatileImageField(upload_to="user-avatars", blank=True, null=True)
    address = models.OneToOneField(
        Address, related_name="address", on_delete=models.CASCADE, blank=True, null=True
    )

    manager = models.ForeignKey('self', null=True, related_name='user', on_delete=models.CASCADE)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        permissions = (
            (
                AccountPermissions.MANAGE_STAFF.codename, 
                pgettext_lazy("Permission description", "Manage staff.")),
            (
                AccountPermissions.IS_TECHNICIAN.codename,
                pgettext_lazy("Permission description", "Is a technician responsible for device maintainance."),
            ),
            (
                AccountPermissions.IS_CONTRACTOR.codename,
                pgettext_lazy("Permission description", "Is a contructor who is a direct customer of KovcoLab."),
            ),
            (
                AccountPermissions.IS_CONTRACTOR_CUSTOMER.codename,
                pgettext_lazy("Permission description", "Is a customer of KovcoLab contructor who actually owns the device."),
            ),
        )


    def get_full_name(self):
        if self.first_name or self.last_name:
            return ("%s %s" % (self.first_name, self.last_name)).strip()
        return self.email

    def get_short_name(self):
        return self.email

    def is_staff(self):
        return self.user_type == CustomerTypes.STAFF

    def is_technician(self):
        return self.user_type == CustomerTypes.TECHNICIAN

    def is_contractor(self):
        return self.user_type == CustomerTypes.CONTRACTOR

    def is_contractor_customer(self):
        return self.user_type == CustomerTypes.CONTRACTOR_CUSTOMER

    def __str__(self):
        return self.email
