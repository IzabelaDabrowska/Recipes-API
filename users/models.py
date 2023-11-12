import random
import string

from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AppUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class AppUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), blank=False, unique=True)
    activation_code = models.CharField(max_length=8, blank=True, null=True)
    activation_code_valid_until = models.DateTimeField(blank=True, null=True)
    objects = AppUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    favorites_recipes = models.ManyToManyField("recipes.Recipe")

    def set_activation_code(self):
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.activation_code = code
        self.activation_code_valid_until = timezone.now() + timezone.timedelta(days=1)

    def send_activation_mail(self):
        send_mail(
            'Complete your registration!',
            f'to complete your registration please enter the following code: {self.activation_code}',
            'recipes@wp.pl',
            [self.email, ],
            fail_silently=False
        )

    def register(self, password):
        self.set_password(password)
        self.is_active = False
        self.set_activation_code()
        self.send_activation_mail()
        self.save()

    def activate(self, activation_code):
        if self.is_active is True:
            raise Exception('User is already activated')
        if self.activation_code != activation_code:
            raise Exception('Provided activation code is invalid')
        if self.activation_code_valid_until < timezone.now():
            raise Exception('Provided activation code expired')
        self.is_active = True
        self.activation_code_valid_until = timezone.now()
        self.save()

    def resend_activation_code(self):
        if self.is_active is True:
            raise Exception('User is already activated')
        self.set_activation_code()
        self.send_activation_mail()
        self.save()
