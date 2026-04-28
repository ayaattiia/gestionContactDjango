from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from contacts.views import SignUpView  # [IMPORTANT] Ne pas oublier cet import

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Système d'authentification (Bonus +2 pts) 
    path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/signup/', SignUpView.as_view(), name='signup'), # Route pour l'inscription
    
    # Ton application (CRUD) [cite: 12]
    path('', include('contacts.urls')), 
] 

# [IMPORTANT] Configuration pour l'affichage des images (Bonus +2 pts) 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)