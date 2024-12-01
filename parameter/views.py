from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

# Create your views here.

from django.shortcuts import render, redirect
from .forms import *
from django.views.generic import ListView, UpdateView, DeleteView,DetailView,CreateView
from .models import *
from School_management import views as cviews
from .forms import PromotionForm, Annee_univForm
from django.contrib import messages
from django.db import IntegrityError




class ContentListView(cviews.CustomListView):
    template_name = "list-x-content.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_add"] = False
        context["can_import"] = False
        context["can_export"] = False
        context["can_delete"] = False
        return context


class MailContentListView(ContentListView):
    model = MailContent
    name = "mail-content"


class MailContentUpdateView(cviews.CustomUpdateView):
    model = MailContent
    form_class = MailContentForm
    name = "mail-content"
    success_url = reverse_lazy("settings:mail-content-list")

    def form_valid(self, form):
        current = get_object_or_404(MailContent, pk=self.kwargs.get("pk"))
        current.is_active = False
        current.save()
        return super().form_valid(form)


class UfrListView(cviews.CustomListView):
    model = UniteDeRecherche
    name = "uniteDeRecherche"
    template_name = "ufr/list-ufr.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add'] = True
        return context


class UfrCreateView(cviews.CustomCreateView):
    model = UniteDeRecherche
    form_class = UniteDeRechercheForm
    name = "uniteDeRecherche"
    success_url = reverse_lazy("parameter:uniteDeRecherche-list")
    


class UfrUpdateView(cviews.CustomUpdateView):
    model = UniteDeRecherche
    name = "uniteDeRecherche"
    form_class = UniteDeRechercheForm
    success_url = reverse_lazy("parameter:ufr-list")


class UfrDetailView(cviews.CustomDetailView):
    model = UniteDeRecherche
    name = "uniteDeRecherche"
    template_name = "ufr/detail-ufr.html"


class UfrDeleteView(cviews.CustomDeleteView):
    model = UniteDeRecherche
    name = "uniteDeRecherche"
    template_name = "ufr/delete-ufr.html"
    success_url = reverse_lazy("parameter:uniteDeRecherche-delete")


##Departement views

class DepartementListView(cviews.CustomListView):
    model = Departement
    name = "departement"
    context_object_name = "departements"
    template_name = "departement/list-departement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DepartementCreateView(cviews.CustomCreateView):
    model = Departement
    form_class = DepartementForm
    name = "departement"
    template_name = "form.html"
    success_url = reverse_lazy("parameter:departement-list")
    


class DepartementUpdateView(cviews.CustomUpdateView):
    model = Departement
    name = "departement"
    form_class = DepartementForm
    success_url = reverse_lazy("parameter:departement-list")


class DepartementDetailView(cviews.CustomDetailView):
    model = Departement
    name = "departement"
    template_name = "departement/detail-departement.html"


class DepartementDeleteView(cviews.CustomDeleteView):
    model = Departement
    name = "departement"
    template_name = "departement/delete-departement.html"
    success_url = reverse_lazy("parameter:departement-list")


##Filieres views

class FiliereListView(cviews.CustomListView):
    model = Filiere
    name = "filiere"
    template_name = "filiere/list-filiere.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FiliereCreateView(cviews.CustomCreateView):
    model = Filiere
    form_class = FiliereForm
    name = "filiere"
    template_name = "form.html"
    success_url = reverse_lazy("parameter:filiere-list")
    


class FiliereUpdateView(cviews.CustomUpdateView):
    model = Filiere
    name = "filiere"
    template_name = "filiere/create_filiere.html"
    form_class = FiliereForm
    success_url = reverse_lazy("parameter:filiere-list")


class FiliereDetailView(cviews.CustomDetailView):
    model = Filiere
    name = "filiere"
    template_name = "filiere/detail-filiere.html"


class FiliereDeleteView(cviews.CustomDeleteView):
    model = Filiere
    name = "filiere"
    template_name = "filiere/delete-filiere.html"
    success_url = reverse_lazy("parameter:filiere-list")
    
    
##semestre views

class SemestreListView(cviews.CustomListView):
    model = Semestre
    name = "semestre"
    template_name = "semestre/list-semestre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SemestreCreateView(cviews.CustomCreateView):
    model = Semestre
    form_class = SemestreForm
    name = "semestre"
    success_url = reverse_lazy("parameter:semestre-list")
    


class SemestreUpdateView(cviews.CustomUpdateView):
    model = Semestre
    name = "semestre"
    form_class = SemestreForm
    success_url = reverse_lazy("parameter:semestre-list")


class SemestreDetailView(cviews.CustomDetailView):
    model = Semestre
    name = "semestre"
    template_name = "semestre/detail-semestre.html"


class SemestreDeleteView(cviews.CustomDeleteView):
    model = Semestre
    name = "semestre"
    template_name = "semestre/delete-semestre.html"
    success_url = reverse_lazy("parameter:semestre-list")
    
    
##UE views

class UeListView(cviews.CustomListView):
    model = UE
    name = "ue"
    template_name = "ue/list-ue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_of"] = "Suppression d'une UE"
        return context


class UeCreateView(cviews.CustomCreateView):
    model = UE
    form_class = UEForm
    name = "ue"
    success_url = reverse_lazy("parameter:ue-list")
    


class UeUpdateView(cviews.CustomUpdateView):
    model = UE
    name = "ue"
    form_class = UEForm
    success_url = reverse_lazy("parameter:ue-list")


class UeDetailView(cviews.CustomDetailView):
    model = UE
    name = "ue"
    template_name = "ue/detail-ue.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Détails de l'UE"
        context["update_url"] = "parameter:ue-update"
        context["delete_url"] = "parameter:ue-delete"
        context["list_url"] = "parameter:ue-list"
        context["list_of"] = "Suppression d'une UE"

        return context

class UeDeleteView(cviews.CustomDeleteView):
    model = UE
    name = "ue"
    template_name = "ue/delete-ue.html"
    success_url = reverse_lazy("parameter:ue-list")
    
    
##Module views

class ModuleListView(cviews.CustomListView):
    model = Module
    name = "module"
    template_name = "modules/list-module.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ModuleCreateView(cviews.CustomCreateView):
    model = Module
    form_class = ModuleForm
    name = "module"
    success_url = reverse_lazy("parameter:module-list")
    


class ModuleUpdateView(cviews.CustomUpdateView):
    model = Module
    name = "module"
    form_class = ModuleForm
    success_url = reverse_lazy("parameter:module-list")


class ModuleDetailView(cviews.CustomDetailView):
    model = Module
    name = "module"
    template_name = "modules/detail-module.html"


class ModuleDeleteView(cviews.CustomDeleteView):
    model = Module
    name = "module"
    template_name = "modules/delete-module.html"
    success_url = reverse_lazy("parameter:module-list")
    
    
##Niveau views

class NiveauListView(cviews.CustomListView):
    model = Niveau
    name = "niveau"
    template_name = "niveau/list-niveau.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NiveauCreateView(cviews.CustomCreateView):
    model = Niveau
    form_class = NiveauForm
    name = "niveau"
    success_url = reverse_lazy("parameter:niveau-list")
    


class NiveauUpdateView(cviews.CustomUpdateView):
    model = Niveau
    name = "niveau"
    form_class = NiveauForm
    success_url = reverse_lazy("parameter:niveau-list")


class NiveauDetailView(cviews.CustomDetailView):
    model = Niveau
    name = "niveau"
    template_name = "niveau/detail-niveau.html"


class NiveauDeleteView(cviews.CustomDeleteView):
    model = Niveau
    name = "niveau"
    template_name = "niveau/delete-niveau.html"
    success_url = reverse_lazy("parameter:niveau-list")
    
# promotion
class PromotionListView(cviews.CustomListView):
    model = Promotion
    name = "promotion"
    template_name = "promotion/list-promotion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PromotionCreateView(cviews.CustomCreateView):
    model = Promotion
    name = "promotion"
    form_class = PromotionForm
    success_url = reverse_lazy("parameter:promotion-list")



class PromotionUpdateView(cviews.CustomUpdateView):
    model = Promotion
    name = "promotion"
    form_class = PromotionForm
    success_url = reverse_lazy("parameter:promotion-list")


class PromotionDetailView(cviews.CustomDetailView):
    model = Promotion
    name = "promotion"
    template_name = "promotion/detail-promotion.html"


class PromotionDeleteView(cviews.CustomDeleteView):
    model = Promotion
    name = "promotion"
    template_name = "promotion/delete-promotion.html"
    success_url = reverse_lazy("parameter:promotion-list")

# Année universitaire

class Annee_univListView(cviews.CustomListView):
    model = Annee_univ
    name = "annee_univ"
    template_name = "annee_univ/list-annee_univ.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class Annee_univCreateView(cviews.CustomCreateView):
    model = Annee_univ
    name = "annee_univ"
    form_class = Annee_univForm
    success_url = reverse_lazy("parameter:annee_univ-list")


class Annee_univUpdateView(cviews.CustomUpdateView):
    model = Annee_univ
    name = "annee_univ"
    form_class = Annee_univForm
    success_url = reverse_lazy("parameter:annee_univ-list")


class Annee_univDetailView(cviews.CustomDetailView):
    model = Annee_univ
    name = "annee_univ"
    template_name = "annee_univ/detail-annee_univ.html"


class Annee_univDeleteView(cviews.CustomDeleteView):
    model = Annee_univ
    name = "annee_univ"
    template_name = "promotion/delete-annee_univ.html"
    success_url = reverse_lazy("parameter:annee_univ-list")





