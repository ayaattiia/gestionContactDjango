from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from .models import Contact


# ===================== HOME =====================
def home_view(request):
    return render(request, 'contacts/home.html')


# ===================== LIST CONTACTS =====================
class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Contact.objects.all()

        # ================= SEARCH =================
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(nom__icontains=search_query) |
                Q(prenom__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(telephone__icontains=search_query)
            )

        # ================= SORT =================
        sort_by = self.request.GET.get('sort', 'date_ajout')
        order = self.request.GET.get('order', 'desc')  # DEFAULT DESC

        valid_sorts = {
            'nom': 'nom',
            'prenom': 'prenom',
            'email': 'email',
            'telephone': 'telephone',
            'date_ajout': 'date_ajout',
        }

        field = valid_sorts.get(sort_by, 'date_ajout')

        # apply order
        if order == 'desc':
            field = f'-{field}'

        # stable sorting (important for pagination)
        if sort_by == 'prenom':
            queryset = queryset.order_by(field, 'nom')
        else:
            queryset = queryset.order_by(field)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', 'date_ajout')
        context['current_order'] = self.request.GET.get('order', 'desc')

        return context


# ===================== DETAIL =====================
class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'
    context_object_name = 'contact'


# ===================== CREATE =====================
class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = 'contacts/contact_form.html'
    fields = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'image', 'category']
    success_url = reverse_lazy('contacts:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# ===================== UPDATE =====================
class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'contacts/contact_form.html'
    fields = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'image', 'category']
    success_url = reverse_lazy('contacts:list')


# ===================== DELETE =====================
class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'contacts/contact_confirm_delete.html'
    success_url = reverse_lazy('contacts:list')


# ===================== SIGN UP =====================
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Contact.objects.all()

        # SEARCH
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(nom__icontains=search_query) |
                Q(prenom__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(telephone__icontains=search_query)
            )

        # SORT
        sort_by = self.request.GET.get('sort', 'date_ajout')
        order = self.request.GET.get('order', 'desc')

        valid_sorts = {
            'nom': 'nom',
            'prenom': 'prenom',
            'email': 'email',
            'telephone': 'telephone',
            'date_ajout': 'date_ajout',
        }

        field = valid_sorts.get(sort_by, 'date_ajout')

        if order == 'desc':
            field = f'-{field}'

        if sort_by == 'prenom':
            queryset = queryset.order_by(field, 'nom')
        else:
            queryset = queryset.order_by(field)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', 'date_ajout')
        context['current_order'] = self.request.GET.get('order', 'desc')

        # ⭐ FIX IMPORTANT : dernier contact réel de la base
        context['dernier_contact'] = Contact.objects.order_by('-date_ajout').first()

        return context