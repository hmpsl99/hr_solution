from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .utils import send_email


class User(AbstractUser):
    class UserRole(models.IntegerChoices):
        regular_employee = 1
        human_resources_manager = 2
        payroll_manager = 3

    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    role = models.IntegerField(default=UserRole.regular_employee, choices=UserRole.choices)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def generate_unique_link(self):
        if not self.is_active:
            self.link = urlsafe_base64_encode(force_bytes(self.email))
        else:
            pass

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.is_active = False
            self.generate_unique_link()
            send_email(user=self, subject="Information Form", template="Hr/email_template.html")

        return super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    national_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.email = f"{self.username}@domain.org"
        return super(Profile, self).save(*args, **kwargs)


class Salary(models.Model):
    user = models.ForeignKey(User, related_name="salaries", on_delete=models.DO_NOTHING, null=True, blank=True)
    balance = models.CharField(max_length=31)
    date = models.DateTimeField(auto_now=True)
