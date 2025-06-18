from django.urls import path

from .views import Welcome

app_name = 'welcome'


urlpatterns = [
    path('', Welcome.as_view(), name='index'),
]
