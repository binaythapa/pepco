from django.urls import path,re_path
from rest_framework.routers import DefaultRouter
from api.views import *
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'file',FileUploadViewSet,'file')
router.register(r'project',ProjectUploadViewSet,'project')
router.register(r'mapping',MappingUploadViewSet,'mapping')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'sql', SqlViewSet, basename='sql')
router.register(r'index', IndexViewSet, basename='index')
router.register(r'terminals', TerminalViewSet, basename='terminals')

urlpatterns = [
    #User Authentication
    re_path('signup', views.signup),
    re_path('login', views.login),
    re_path('test_token', views.test_token),    
    path('', include(router.urls)),
    path('validate/', Validator.as_view(), name='validate'),
    path('validate/<int:project_id>/', Validator.as_view(), name='validate'),
    path('terminal/<int:project_id>/', Terminal.as_view(), name='terminal'),
]
