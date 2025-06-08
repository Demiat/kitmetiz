from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

from .constants import MIN_CODE, MAX_CODE

User = get_user_model()


class EmailVerificationForm(forms.Form):
    """Форма ввода email для отправки кода проверки."""

    email = forms.EmailField(label='', help_text='Электронная почта')


class CustomUserCreationForm(UserCreationForm):
    """Форма создания пользователя."""

    verification_code = forms.IntegerField(
        min_value=MIN_CODE,
        max_value=MAX_CODE,
        label='Код подтверждения',
        help_text='Введите код из письма.',
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)
