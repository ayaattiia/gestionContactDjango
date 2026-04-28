from django.contrib import admin
from .models import Contact,Category

admin.site.register(Contact)
admin.site.register(Category)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'date_ajout')
    list_filter = ('date_ajout',)
    search_fields = ('nom', 'prenom', 'email', 'telephone')
    ordering = ('nom', 'prenom')