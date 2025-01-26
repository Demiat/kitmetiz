from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm

User = get_user_model()


class RegisterUserView(CreateView):
    """Регистрация пользователя"""

    model = User
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Отправляем письмо после успешной регистрации
        send_mail(
            'Успешная регистрация',
            f"""Поздравляем! {form.cleaned_data['username']} Вы успешно
            зарегистрировались на нашем сайте.""",
            'demiat@mail.ru',
            (form.cleaned_data['email'],),
            fail_silently=True
        )

        return response


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
