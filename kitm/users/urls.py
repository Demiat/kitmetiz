from django.urls import path, include

from users.views import (
    RegisterUserView, UserProfile, EditProfile, activate_user
)

app_name = 'users'

urlpatterns = [
    path('registration/', RegisterUserView.as_view(), name='registration'),
    path(
        'activate/<slug:uidb64>/<slug:token>/',
        activate_user,
        name='activate'
    ),
    path('profile/<username>/', UserProfile.as_view(), name='profile'),
    path('edit/profile/', EditProfile.as_view(), name='edit_profile'),
    path('', include('django.contrib.auth.urls')),
]
