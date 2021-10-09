from django.contrib import admin
from core.custom_admin import custom_admin_site
from .models import TestModel

admin.site.register(TestModel)
custom_admin_site.register(TestModel)