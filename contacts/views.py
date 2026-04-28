from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .models import Contact

from django.shortcuts import render

def home_view(request):
    return render(request, 'contacts/home.html')
class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 5 # Active la pagination

    def get_queryset(self):
        # 1. On récupère les contacts (tu peux filtrer par utilisateur si besoin)
        # queryset = Contact.objects.filter(user=self.request.user) 
        queryset = Contact.objects.all()

        # 2. Gestion de la recherche
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(nom__icontains=search_query) |
                Q(prenom__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(telephone__icontains=search_query)
            )

        # 3. Gestion du tri
        sort_by = self.request.GET.get('sort', 'nom')
        if sort_by == 'date_ajout':
            queryset = queryset.order_by('-date_ajout')
        elif sort_by == 'prenom':
            queryset = queryset.order_by('prenom', 'nom')
        else:
            queryset = queryset.order_by('nom', 'prenom')
            
        return queryset

    def get_context_data(self, **kwargs):
        # Permet de garder les variables dans le template (pour la barre de recherche)
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', 'nom')
        return context

class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'
    context_object_name = 'contact'

class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = 'contacts/contact_form.html'
    fields = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'image', 'category']
    success_url = reverse_lazy('contacts:list')

    def form_valid(self, form):
        form.instance.user = self.request.user # ou owner selon ton modèle
        return super().form_valid(form)

class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'contacts/contact_form.html'
    fields = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'image', 'category']
    success_url = reverse_lazy('contacts:list')

class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'contacts/contact_confirm_delete.html'
    success_url = reverse_lazy('contacts:list')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'