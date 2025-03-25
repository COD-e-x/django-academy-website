from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


NULLABLE = {"null": True, "blank": True}
NULLABLE_FOR_STRING = {"null": False, "blank": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name=_("Эл. почта"))
    phone = models.CharField(
        max_length=35,
        verbose_name=_("Номер телефона"),
        **NULLABLE_FOR_STRING,
    )
    telegram = models.CharField(
        max_length=150,
        verbose_name=_("Телеграм"),
        **NULLABLE_FOR_STRING,
    )
    birth_date = models.DateField(
        **NULLABLE,
        verbose_name=_("Дата рождения"),
    )
    address = models.CharField(
        max_length=255,
        **NULLABLE_FOR_STRING,
        verbose_name=_("Адрес"),
    )
    gender = models.CharField(
        max_length=1,
        choices=[
            ("М", _("Мужской")),
            ("Ж", _("Женский")),
        ],
        verbose_name=_("Пол"),
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        **NULLABLE,
        verbose_name=_("Фото профиля"),
    )
    status = models.CharField(
        max_length=10,
        choices=[
            ("active", _("Активный")),
            ("inactive", _("Неактивный")),
            ("banned", _("Заблокирован")),
        ],
        default="active",
        verbose_name=_("Статус"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Активен"),
    )

    # phone_verified = models.BooleanField(default=False, verbose_name=_("Телефон подтверждён"))
    # telegram_verified = models.BooleanField(default=False, verbose_name=_("Telegram подтверждён"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ["id"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()
