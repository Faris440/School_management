from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.

from django.shortcuts import render, redirect
from .forms import *
from django.views.generic import ListView, UpdateView, DeleteView,DetailView,CreateView
from .models import *



class UfrListView(ListView):
    model = UniteDeRecherche
    name = "ufr"
    context_object_name = "ufrs"
    template_name = "ufr/list-ufr.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UfrCreateView(CreateView):
    model = UniteDeRecherche
    form_class = UniteDeRechercheForm
    name = "ufr"
    template_name = "ufr/create_unite_de_recherche.html"
    success_url = reverse_lazy("parameter:ufr-list")
    


class UfrUpdateView(UpdateView):
    model = UniteDeRecherche
    name = "ufr"
    template_name = "ufr/create_unite_de_recherche.html"
    form_class = UniteDeRechercheForm
    success_url = reverse_lazy("parameter:ufr-list")


class UfrDetailView(DetailView):
    model = UniteDeRecherche
    name = "ufr"
    template_name = "ufr/detail-ufr.html"


class UfrDeleteView(DeleteView):
    model = UniteDeRecherche
    name = "ufr"
    template_name = "ufr/delete-ufr.html"
    success_url = reverse_lazy("parameter:ufr-list")


##Departement views

class DepartementListView(ListView):
    model = Departement
    name = "departement"
    context_object_name = "departements"
    template_name = "departement/list-departement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DepartementCreateView(CreateView):
    model = Departement
    form_class = DepartementForm
    name = "departement"
    template_name = "departement/create_departement.html"
    success_url = reverse_lazy("parameter:departement-list")
    


class DepartementUpdateView(UpdateView):
    model = Departement
    name = "departement"
    template_name = "departement/create_departement.html"
    form_class = DepartementForm
    success_url = reverse_lazy("parameter:departement-list")


class DepartementDetailView(DetailView):
    model = Departement
    name = "departement"
    template_name = "departement/detail-departement.html"


class DepartementDeleteView(DeleteView):
    model = Departement
    name = "departement"
    template_name = "departement/delete-departement.html"
    success_url = reverse_lazy("parameter:departement-list")


##Filieres views

class FiliereListView(ListView):
    model = Filiere
    name = "filiere"
    context_object_name = "filieres"
    template_name = "filiere/list-filiere.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FiliereCreateView(CreateView):
    model = Filiere
    form_class = FiliereForm
    name = "filiere"
    template_name = "filiere/create_filiere.html"
    success_url = reverse_lazy("parameter:filiere-list")
    


class FiliereUpdateView(UpdateView):
    model = Filiere
    name = "filiere"
    template_name = "filiere/create_filiere.html"
    form_class = FiliereForm
    success_url = reverse_lazy("parameter:filiere-list")


class FiliereDetailView(DetailView):
    model = Filiere
    name = "filiere"
    template_name = "filiere/detail-filiere.html"


class FiliereDeleteView(DeleteView):
    model = Filiere
    name = "filiere"
    template_name = "filiere/delete-filiere.html"
    success_url = reverse_lazy("parameter:filiere-list")
    
    
##semestre views

class SemestreListView(ListView):
    model = Semestre
    name = "semestre"
    context_object_name = "semestres"
    template_name = "semestre/list-semestre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SemestreCreateView(CreateView):
    model = Semestre
    form_class = SemestreForm
    name = "semestre"
    template_name = "semestre/create_semestre.html"
    success_url = reverse_lazy("parameter:semestre-list")
    


class SemestreUpdateView(UpdateView):
    model = Semestre
    name = "semestre"
    template_name = "semestre/create_semestre.html"
    form_class = SemestreForm
    success_url = reverse_lazy("parameter:semestre-list")


class SemestreDetailView(DetailView):
    model = Semestre
    name = "semestre"
    template_name = "semestre/detail-semestre.html"


class SemestreDeleteView(DeleteView):
    model = Semestre
    name = "semestre"
    template_name = "semestre/delete-semestre.html"
    success_url = reverse_lazy("parameter:semestre-list")
    
    
##UE views

class UeListView(ListView):
    model = UE
    name = "ue"
    context_object_name = "ues"
    template_name = "ue/list-ue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UeCreateView(CreateView):
    model = UE
    form_class = UEForm
    name = "ue"
    template_name = "ue/create_ue.html"
    success_url = reverse_lazy("parameter:ue-list")
    


class UeUpdateView(UpdateView):
    model = UE
    name = "ue"
    template_name = "ue/create_ue.html"
    form_class = UEForm
    success_url = reverse_lazy("parameter:ue-list")


class UeDetailView(DetailView):
    model = UE
    name = "ue"
    template_name = "ue/detail-ue.html"


class UeDeleteView(DeleteView):
    model = UE
    name = "ue"
    template_name = "ue/delete-ue.html"
    success_url = reverse_lazy("parameter:ue-list")
    
    
##Module views

class ModuleListView(ListView):
    model = Module
    name = "module"
    context_object_name = "modules"
    template_name = "module/list-module.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ModuleCreateView(CreateView):
    model = Module
    form_class = ModuleForm
    name = "module"
    template_name = "module/create_module.html"
    success_url = reverse_lazy("parameter:module-list")
    


class ModuleUpdateView(UpdateView):
    model = Module
    name = "module"
    template_name = "module/create_module.html"
    form_class = ModuleForm
    success_url = reverse_lazy("parameter:module-list")


class ModuleDetailView(DetailView):
    model = Module
    name = "module"
    template_name = "module/detail-module.html"


class ModuleDeleteView(DeleteView):
    model = Module
    name = "module"
    template_name = "module/delete-module.html"
    success_url = reverse_lazy("parameter:module-list")
    
    
##Niveau views

class NiveauListView(ListView):
    model = Niveau
    name = "niveau"
    context_object_name = "niveaux"
    template_name = "niveau/list-niveau.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NiveauCreateView(CreateView):
    model = Niveau
    form_class = NiveauForm
    name = "niveau"
    template_name = "niveau/create_niveau.html"
    success_url = reverse_lazy("parameter:niveau-list")
    


class NiveauUpdateView(UpdateView):
    model = Niveau
    name = "niveau"
    template_name = "niveau/create_niveau.html"
    form_class = NiveauForm
    success_url = reverse_lazy("parameter:niveau-list")


class NiveauDetailView(DetailView):
    model = Niveau
    name = "niveau"
    template_name = "niveau/detail-niveau.html"


class NiveauDeleteView(DeleteView):
    model = Niveau
    name = "niveau"
    template_name = "niveau/delete-niveau.html"
    success_url = reverse_lazy("parameter:niveau-list")
    
    
    
    
    




