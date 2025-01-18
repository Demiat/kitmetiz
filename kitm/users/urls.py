from django.urls import path

from users.views import RegisterUserView, UserProfile, EditProfile

app_name = 'users'

urlpatterns = [
    path('registration/', RegisterUserView.as_view(), name='registration'),
    path('profile/<username>/', UserProfile.as_view(), name='profile'),
    path('edit/profile/', EditProfile.as_view(), name='edit_profile'),
]
