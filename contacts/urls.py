from django.urls import path
from . import views
from .views import ContactListView, home_view  # Ajoute home_view ici


app_name = 'contacts'

urlpatterns = [
    path('', home_view, name='home'),  # La page d'accueil esthétique
    path('list/', ContactListView.as_view(), name='list'), # La liste avec pagination
    path('ajouter/', views.ContactCreateView.as_view(), name='add'),
    path('<int:pk>/', views.ContactDetailView.as_view(), name='detail'),
    path('modifier/<int:pk>/', views.ContactUpdateView.as_view(), name='edit'),
    path('supprimer/<int:pk>/', views.ContactDeleteView.as_view(), name='delete'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
]
