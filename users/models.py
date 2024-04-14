from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from events.models_auxiliary import Direction


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    EXPERIENCE_CHOICES = (
        ('no_experience', 'Нет опыта'),
        ('from_one_year', 'От 1 года'),
        ('from_3_years', 'От 3 лет'),
        ('from_5_years', 'От 5 лет'),
        ('other', 'Другое'),
    )

    username = None
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    middle_name = models.CharField(blank=True, max_length=256)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(
        validators=[phone_number_regex],
        max_length=16, unique=True, blank=True)
    telegram = models.CharField(blank=True, max_length=128)
    job = models.CharField(blank=True, max_length=256)
    job_title = models.CharField(blank=True, max_length=256)
    experience = models.CharField(
        choices=EXPERIENCE_CHOICES,
        blank=True, max_length=128)
    direction = models.ManyToManyField(
        Direction, related_name='users', blank=True,
        verbose_name='preferred directions')
    image = models.ImageField(
        upload_to='users/images/',
        blank=True,
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['email']
        app_label = 'users'
        verbose_name = ("user")
        verbose_name_plural = ("users")

    def __str__(self):
        return self.email
