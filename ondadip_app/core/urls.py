from django.urls import path

from . import views


app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('security/<int:security_id>/', views.security, name='security'),
    path('user/<int:user_id>/portfolio/', views.portfolio, name='portfolio'),
]