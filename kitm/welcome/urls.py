from django.urls import path

from .views import Welcome

app_name = 'welcome'


urlpatterns = [
    path('', Welcome.as_view(), name='index'),
    path('<slug:cat_slug>/', Welcome.as_view(), name='index'),
]
