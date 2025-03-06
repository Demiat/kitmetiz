from django.urls import reverse
from pytest import fixture
from django.test import Client

HOME_PAGE = reverse('welcome:index')
ABOUT_PAGE = reverse('pages:about')
CONTACT_PAGE = reverse('pages:contact')
REGISTRATION_PAGE = reverse('users:registration')


@fixture
def author(django_user_model):
    """Создает автора."""
    return django_user_model.objects.create(username='ivan_author')


@fixture
def profile_url(author):
    """Возвращает ссылку на профиль автора."""
    return reverse('users:profile', kwargs={'username': author.username})


@fixture
def author_client(author):
    """Логинит автора."""
    client = Client()
    client.force_login(author)
    return client
