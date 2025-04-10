from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
    path('test-openai/', views.test_openai, name='test_openai'),
    path('debug/', views.debug_info, name='debug_info'),
]