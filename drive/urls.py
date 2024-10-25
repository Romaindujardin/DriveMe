from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),  # URL racine redirige vers la page 'home'
    path('login/', views.login_view, name='login'),
    path('signin/', views.signin_view, name='signin'),
    path('home/', views.home_view, name='home'),
    path('main/', views.main_view, name='main'),  # Assure-toi d'avoir cette vue
    path('logout/', views.logout_view, name='logout'),
]



