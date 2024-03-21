from django.contrib import admin
from .models import *

from django.contrib import admin

admin.site.site_header = 'Logic Data Validation'

# Register your models here.
admin.site.register(File)
admin.site.register(Project)
admin.site.register(Mapping)
admin.site.register(Index)
admin.site.register(Sql)
admin.site.register(Category)
admin.site.register(Terminal)
