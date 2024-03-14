
from django.contrib import admin
from django.urls import path, include
from api.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [   
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('account', include('account.urls')),    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
