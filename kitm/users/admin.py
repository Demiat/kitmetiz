from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from core.admin import сustom_admin_site

сustom_admin_site.register(CustomUser, UserAdmin)
