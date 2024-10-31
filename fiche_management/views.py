from django.shortcuts import render
from formset.views import FormCollectionView
from django.views.generic import ListView
from .forms import FinalFormCollection
from .models import Sheet, Enseignements
from django.contrib import messages
from School_management import views as cviews
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse

# Create your views here.
class SheetCreateView(cviews.CustomFormCollectionView):
    model = Sheet
    name = "sheet"
    collection_class = FinalFormCollection
    
    def get_success_url(self):
        return reverse('fiche_management:sheet-list')
    
    
    def form_collection_valid(self, form_collection):
        sheet_data = form_collection.cleaned_data['sheet']
        enseignement_data = form_collection.cleaned_data['enseignement']
        sheet = Sheet.objects.create(
            enseignant = sheet_data['enseignant'],
            date_debut = sheet_data['date_debut'],
            date_fin = sheet_data['date_fin'],
        )

        enseignements = Enseignements.objects.create(
            code = enseignement_data['code'],
            sheet = sheet,
            filiere = enseignement_data['filiere'],
            niveau = enseignement_data['niveau'],
            semestre = enseignement_data['semestre'],
            module = enseignement_data['module'],
            ct_volume_horaire_confie = enseignement_data['ct_volume_horaire_confie'],
            td_volume_horaire_confie = enseignement_data['td_volume_horaire_confie'],
            tp_volume_horaire_confie = enseignement_data['tp_volume_horaire_confie'],
            ct_volume_horaire_efectue = enseignement_data['ct_volume_horaire_efectue'],
            td_volume_horaire_efectue = enseignement_data['td_volume_horaire_efectue'],
            tp_volume_horaire_efectue = enseignement_data['tp_volume_horaire_efectue'],
        )
        messages.success(self.request, f'Le dossier a été enregistré avec succès!')
        return JsonResponse({'success_url': self.get_success_url()})
    
    
class SheetListView(cviews.CustomListView):
    model = Sheet
    name = "sheet"
    template_name = "list-sheet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SheetDetailView(cviews.CustomDetailView):
    model = Sheet
    template_name = "detail-sheet.html"  # Remplacez par le chemin de votre template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


class SheetUpdateView(cviews.CustomUpdateView):
    model = Sheet
    fields = "__all__"  # Spécifiez les champs que vous voulez afficher dans le formulaire

    def get_success_url(self):
        return reverse('fiche_management:sheet-list')  # Redirige vers la liste après la mise à jour

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


class SheetDeleteView(cviews.CustomDeleteView):
    model = Sheet
    template_name = "sheet_confirm_delete.html"  # Remplacez par le chemin de votre template
    success_url = reverse_lazy('fiche_management:sheet-list')  # Redirige vers la liste après la suppression

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




# class SheetUpdateView(cviews.CustomUpdateView):
#     model = Sheet
#     name = "sheet"
#     context_object_name = "sheets"
#     template_name = "update-sheet.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
    
# class SheetDetailView(cviews.CustomDetailView):
#     model = Sheet
#     name = "sheet"
#     context_object_name = "sheets"
#     template_name = "detail-sheet.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
    
# class SheetDeleteView(cviews.CustomDeleteView):
#     model = Sheet
#     name = "sheet"
#     context_object_name = "sheets"
#     template_name = "delete-sheet.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
    
