from django.urls import path, include

from users.views import RegisterUserView, UserProfile, EditProfile

app_name = 'users'

urlpatterns = [
    path('registration/', RegisterUserView.as_view(), name='registration'),
    path('profile/<username>/', UserProfile.as_view(), name='profile'),
    path('edit/profile/', EditProfile.as_view(), name='edit_profile'),
    path('', include('django.contrib.auth.urls')),
]
