from http import HTTPStatus

from pytest import mark, lazy_fixture
from pytest_django.asserts import assertRedirects
from django.urls import reverse

from .conftest import (
    HOME_PAGE,
    ABOUT_PAGE,
    CONTACT_PAGE,
    REGISTRATION_PAGE,
)

pytestmark = mark.django_db


@mark.parametrize(
    'revers_name',
    (
        HOME_PAGE,
        ABOUT_PAGE,
        CONTACT_PAGE,
        REGISTRATION_PAGE,
        (reverse('users:login')),
    )
)
def test_anonim_to_home_page(client, revers_name):
    """Доступ Анонима к общим страницам"""
    assert client.get(revers_name).status_code == HTTPStatus.OK, (
        'Доступ Анонима к странице {} невозможен'.format(revers_name)
    )


def test_anonim_redirect_to_login(client, profile_url):
    """Аноним перенаправляется на страницу логина"""
    responce = client.get(profile_url, follow=False)
    assertRedirects(
        responce,
        f'{reverse('users:login')}?next={profile_url}',
        fetch_redirect_response=False
    )


def user_can_view_pages(author_client, profile_url):
    """Авторизованный пользователь может просматривать страницы"""
    responce = author_client.get(profile_url)
    assert responce.status_code == HTTPStatus.OK
