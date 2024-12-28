from django.urls import path, include

from users.views import RegisterUserView

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        RegisterUserView.as_view(),
        name='registration'),
]
