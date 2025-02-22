from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import create_folder, delete_folder, rename_folder, upload_folder, affilier_document
from .views import folder_document_list, download_file, folder_list, rename_document, delete_document ,stats

urlpatterns = [
    path('', views.home_view, name='home'),  # URL racine redirige vers la page 'home'
    path('login/', views.login_view, name='login'),
    path('signin/', views.signin_view, name='signin'),
    path('home/', views.home_view, name='home'),
    path('main/', views.main_view, name='main'),  # Assure-toi d'avoir cette vue
    path('logout/', views.logout_view, name='logout'),
    path('files/', views.files_view, name='files'),
    path('folder/', views.folder_view, name='folder'),
    path('search/', views.search_documents, name='search'),
    path('documents/', views.document_list, name='document_list'),
    path('create-folder/', create_folder, name='create_folder'),
    path('delete-folder/<int:folder_id>/', delete_folder, name='delete_folder'),
    path('rename-folder/<int:folder_id>/', rename_folder, name='rename_folder'),
    path('upload_folder/<int:folder_id>/', upload_folder, name='upload_folder'),
    path('affilier_document/<int:document_id>/', affilier_document, name='affilier_document'),
    path('folder/<int:folder_id>/', folder_document_list, name='folder_documents'),
    path('download/<int:file_id>/', download_file, name='download_file'),
    path('folders/', folder_list, name='folder_list'), 
    path('upload/', views.upload_document, name='upload_document'),
    path('documents/rename/<int:document_id>/', rename_document, name='rename_document'), 
    path('documents/delete/<int:document_id>/', delete_document, name='delete_document'),
    path('stats/',views.stats, name='stats'),#La vue des statistiques
    path('view/<int:document_id>/', views.view_document, name='view_document'),
    # Favoris
    path('favorites/', views.favorites, name='favorites'),
    # Ajouter ou retirer un dossier ou un fichier des favoris
    path('folder/<int:folder_id>/add_favorite_folder/', views.add_favorite_folder, name='add_favorite_folder'),
    path('folder/<int:folder_id>/remove_favorite_folder/', views.remove_favorite_folder, name='remove_favorite_folder'),
    path('document/<int:document_id>/add_favorite_file/', views.add_favorite_file, name='add_favorite_file'),
    path('document/<int:document_id>/remove_favorite_file/', views.remove_favorite_file, name='remove_favorite_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

