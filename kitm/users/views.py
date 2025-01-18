from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm

User = get_user_model()


class RegisterUserView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

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


def user_profile(request, username):
    pass
    # """Управляет профилем пользователя"""
    # profile = get_object_or_404(User, username=username)
    # posts_of_user = profile.posts.select_related(
    #     'category', 'location').annotate(
    #         comment_count=Count('comments')
    # ).order_by('-pub_date')
    # context = {
    #     'profile': profile,
    #     'page_obj': pagination(posts_of_user, request.GET.get('page'))
    # }
    # return render(request, 'blog/profile.html', context)


class UserProfile(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'users/profile.html'


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
