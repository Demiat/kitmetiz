from django.urls import path

from . import views

app_name: str = 'pages'

urlpatterns = [
    path('about/', views.About.as_view(), name='about'),
    path('rules/', views.Contact.as_view(), name='contact'),
]
