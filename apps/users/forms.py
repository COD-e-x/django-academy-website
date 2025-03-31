from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import authenticate
from .models import User

import logging

logger = logging.getLogger(__name__)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        min_length=8,
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput,
        min_length=8,
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        """Валидация пароля."""
        cd = self.cleaned_data
        password1 = cd.get("password")
        password2 = cd.get("password2")
        if password1 != password2:
            raise ValidationError("Пароли не совпадают!")
        return password2

    def clean_email(self):
        """Валидация email"""
        email = self.cleaned_data.get("email").strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Некорректный email!")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован!")
        return email


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        min_length=8,
    )

    def clean_email(self):
        """Валидация email"""
        email = self.cleaned_data.get("email").strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Некорректный email!")
        return email

    def clean(self):
        """Проверка на существование пользователя в базе данных."""
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            logger.info(f"if email and password - email: {email}")
            user = authenticate(email=email, password=password)
            if not user:
                logger.error(f"Неверный email или пароль для {email}")
                raise ValidationError("Неверный email или пароль!")
            if not user.is_active:
                logger.warning(f"Аккаунт заблокирован для {email}")
                raise ValidationError("Этот аккаунт заблокирован!")
        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        exclude = ("is_active", "status")
