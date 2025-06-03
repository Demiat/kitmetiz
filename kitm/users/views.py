from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode
)
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from .forms import CustomUserCreationForm

User = get_user_model()


class RegisterUserView(CreateView):
    """Регистрация пользователя"""

    model = User
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Генерируем уникальный токен для активации
        # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        # token = default_token_generator.make_token(user)

        # Формируем ссылку активации
        # link = reverse(
        #     'users:activate',
        #     kwargs={'uidb64': uidb64, 'token': token}
        # )
        # full_link = f"{self.request.get_host()}{link}"

        # Отправляем письмо с ссылкой на активацию
        send_mail(
            'Активируйте вашу учетную запись',
            f"""Пожалуйста, подтвердите регистрацию пройдя по следующей ссылке:
            http://{self.request.get_host()}{reverse(
                'users:activate',
                kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                }
            )}
            """,
            settings.EMAIL_HOST_USER,
            (form.cleaned_data['email'],),
            fail_silently=True
        )

        return super().form_valid(form)


def activate_user(request, uidb64, token): pass
    # try:
    #     uid = force_text(urlsafe_base64_decode(uidb64))
    #     user = User.objects.get(pk=uid)

    #     if default_token_generator.check_token(user, token):
    #         user.is_active = True
    #         user.save()

    #          # Отправляем письмо после успешной активации
        # send_mail(
        #     'Успешная регистрация',
        #     f"""Поздравляем! {user}, Вы успешно
        #     активировали учетную запись на нашем сайте.""",
        #     'demiat@mail.ru',
        #     (form.cleaned_data['email'],),
        #     fail_silently=True
        # )
    #         return redirect('users:login')
    #     else:
    #         messages.error(request, 'Ссылка недействительна или устарела.')
    #         return redirect('users:register')
    # except Exception as e:
    #     print(e)
    #     messages.error(request, 'Что-то пошло не так.')
    #     return redirect('users:register')


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
    """Редактирование профиля пользователя"""

    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'users/user.html'

    def get_object(self):
        """Предоставляем объект модели для представления"""
        return self.request.user

    def get_success_url(self):
        """Переходит в профиль пользователя после обновления объекта"""
        # Получаем имя пользователя после редактирования профиля
        username = self.object.username
        return reverse('users:profile', args=(username,))
