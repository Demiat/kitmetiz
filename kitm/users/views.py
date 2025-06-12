from random import randint

from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from .forms import CustomUserCreationForm, EmailVerificationForm
from .constants import MIN_CODE, MAX_CODE

User = get_user_model()
SITE = 'http://localhost:8000/'
SEND_MAIL_MSG = (
    'Пожалуйста, подтвердите регистрацию пройдя по следующей ссылке: {}'
)
VERIFICATION_CODE = 'verification_code'
NOT_EMAIL = 'Email не найден!'
WRONG_CODE = 'Неверный код подтверждения!'


def send_code_to_email(request):
    """Отправляет код для подтверждения email."""
    if not request.method == 'POST':
        if request.session.get('email'):
            return redirect('registration')
        return render(
            request,
            'registration/verify_email.html',
            {'form': EmailVerificationForm()}
        )
    form = EmailVerificationForm(request.POST)
    if form.is_valid():
        confirmation_code = randint(MIN_CODE, MAX_CODE)
        request.session[VERIFICATION_CODE] = confirmation_code
        request.session['email'] = form.cleaned_data['email']

        send_mail(
            f'Активируйте вашу учетную запись для {SITE}',
            f'Код подтверждения: {confirmation_code}',
            settings.EMAIL_HOST_USER,
            (form.cleaned_data['email'],),
            fail_silently=True
        )
        return redirect('registration')


class RegisterUserView(CreateView):
    """Регистрация пользователя"""

    model = User
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy(settings.LOGIN_URL)

    def form_valid(self, form):
        user = form.save(commit=False)
        entered_code = form.cleaned_data[VERIFICATION_CODE]
        session_code = self.request.session.get(VERIFICATION_CODE)
        if not self.request.session.get('email'):
            form.add_error(None, NOT_EMAIL)
            return self.form_invalid(form)
        if not session_code or entered_code != session_code:
            form.add_error(VERIFICATION_CODE, WRONG_CODE)
            return self.form_invalid(form)
        user.email = self.request.session.get('email')
        user.save()
        del self.request.session[VERIFICATION_CODE]
        del self.request.session['email']

        return super().form_valid(form)


class UserProfile(LoginRequiredMixin, TemplateView):
    """Просмотр профиля пользователя"""

    model = User
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        """Передает в шаблон информацию"""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя."""

    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'users/user.html'

    def get_object(self):
        """Предоставляем объект модели для обновления."""
        return self.request.user

    def get_success_url(self):
        """Переходит в профиль пользователя после обновления объекта."""
        # Получаем имя пользователя после редактирования профиля
        username = self.object.username
        return reverse('users:profile', args=(username,))
