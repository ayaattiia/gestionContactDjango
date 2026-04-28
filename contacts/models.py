from django.db import models
from django.contrib.auth.models import User # Pour lier le contact à un utilisateur

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Contact(models.Model):
    # L'utilisateur qui a créé le contact (important pour que chacun ait ses propres contacts)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    adresse = models.TextField(blank=True, null=True)
    
    # Ajout d'une photo de profil
    image = models.ImageField(upload_to='contacts_pics/', default='default.png')
    
    # Ajout d'une catégorie (Famille, Travail, etc.)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"