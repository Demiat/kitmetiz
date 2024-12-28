from django.urls import path

from .views import Welcome

app_name: str = 'welcome'


urlpatterns = [
    path('', Welcome.as_view(), name='index'),
]
