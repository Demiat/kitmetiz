from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.admin import сustom_admin_site
from core.views import set_rating_nomenclature
from users.views import RegisterUserView

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('auth/registration/',
         RegisterUserView.as_view(), name='registration'),
    path('auth/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('admin/', сustom_admin_site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('welcome.urls', namespace='welcome')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
