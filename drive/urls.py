from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home_view, name='home'),  # URL racine redirige vers la page 'home'
    path('login/', views.login_view, name='login'),
    path('signin/', views.signin_view, name='signin'),
    path('home/', views.home_view, name='home'),
    path('main/', views.main_view, name='main'),  # Assure-toi d'avoir cette vue
    path('logout/', views.logout_view, name='logout'),
    path('documents/', views.document_list, name='document_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

