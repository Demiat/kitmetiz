from django.urls import path

from users.views import (
    UserProfile, EditProfile,
    send_code_to_email,
)

app_name = 'users'

urlpatterns = [
    path('verify-email/', send_code_to_email, name='verify_email'),
    path('profile/<username>/', UserProfile.as_view(), name='profile'),
    path('edit/profile/', EditProfile.as_view(), name='edit_profile'),
]
