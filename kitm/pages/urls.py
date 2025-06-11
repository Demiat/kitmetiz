from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.About.as_view(), name='about'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('nom_card_detail/<uuid:pk>/',
         views.NomenclatureCardDetail.as_view(), name='nom_card_detail'),
]
