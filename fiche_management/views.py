from django.shortcuts import render
from formset.views import FormCollectionView
from django.views.generic import ListView
from .forms import FinalFormCollection, FinalSelfFormCollection, SheetForm,SheetSelfForm
from .models import Sheet, Enseignements
from django.contrib import messages
from School_management import views as cviews
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

# Create your views here.
class SheetCreateView(cviews.CustomFormCollectionView):
    model = Sheet
    name = "sheet"
    collection_class = FinalFormCollection
    
    def get_collection_class(self):
        user = self.request.user
        if not user.is_staff :
            return FinalSelfFormCollection 
        return FinalFormCollection
    
    def get_success_url(self):
        return reverse('fiche_management:sheet-list')
    
    
    def form_collection_valid(self, form_collection):
        sheet_data = form_collection.cleaned_data.get('sheet')
        enseignement_data = form_collection.cleaned_data.get('enseignement')
        user = self.request.user
        if not user.is_staff :
            sheet = Sheet.objects.create(
            enseignant = user,
            date_debut = sheet_data['date_debut'],
            date_fin = sheet_data['date_fin'],
            )
        else :
            sheet = Sheet.objects.create(
            enseignant = sheet_data['enseignant'],
            date_debut = sheet_data['date_debut'],
            date_fin = sheet_data['date_fin'],
            )
        

        for ens in enseignement_data :
            enseignement = ens['log']
        
            enseignements = Enseignements.objects.create(
                code = enseignement['code'],
                sheet = sheet,
                filiere = enseignement['filiere'],
                niveau = enseignement['niveau'],
                semestre = enseignement['semestre'],
                module = enseignement['module'],
                ct_volume_horaire_confie = enseignement['ct_volume_horaire_confie'],
                td_volume_horaire_confie = enseignement['td_volume_horaire_confie'],
                tp_volume_horaire_confie = enseignement['tp_volume_horaire_confie'],
                ct_volume_horaire_efectue = enseignement['ct_volume_horaire_efectue'],
                td_volume_horaire_efectue = enseignement['td_volume_horaire_efectue'],
                tp_volume_horaire_efectue = enseignement['tp_volume_horaire_efectue'],
            )
        
        messages.success(self.request, f'Le dossier a été enregistré avec succès!')
        return JsonResponse({'success_url': self.get_success_url()})
    
    
class SheetListView(cviews.CustomListView):
    model = Sheet
    name = "sheet"
    template_name = "list-sheet.html"
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_staff :
            return Sheet.objects.filter(enseignant = user)
        return super().get_queryset()

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
    form_class = SheetForm  # Spécifiez les champs que vous voulez afficher dans le formulaire

    def get_success_url(self):
        return reverse('fiche_management:sheet-list')  # Redirige vers la liste après la mise à jour

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        form.instance.motif_de_rejet = None
        form.instance.is_validated = None
        return super().form_valid(form)
    


class SheetDeleteView(cviews.CustomDeleteView):
    model = Sheet
    template_name = "sheet_confirm_delete.html"  # Remplacez par le chemin de votre template
    success_url = reverse_lazy('fiche_management:sheet-list')  # Redirige vers la liste après la suppression

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
def valider_fiche(request, pk):
    # Récupère la fiche avec l'ID fourni ou retourne 404 si elle n'existe pas
    fiche = get_object_or_404(Sheet, id=pk)

    # Vérifie si la fiche est déjà validée
    if fiche.is_validated:
        messages.warning(request, "Cette fiche a déjà été validée.")
    else:
        # Met à jour le statut de validation
        fiche.is_validated = True
        fiche.save()
        messages.success(request, "La fiche a été validée avec succès !")

    return redirect( 'fiche_management:sheet-detail', pk=fiche.id) 


def rejeter_fiche(request, pk):
    fiche = get_object_or_404(Sheet, id=pk)

    if request.method == "POST":
        motif_rejet = request.POST.get("motif_rejet")
        
        if motif_rejet:
            fiche.is_validated = False
            fiche.motif_de_rejet = motif_rejet
            fiche.save()
            messages.success(request, "La fiche a été rejetée avec le motif indiqué.")
            return redirect( 'fiche_management:sheet-detail', pk=fiche.id) 
        else:
            messages.error(request, "Veuillez fournir un motif pour le rejet.")
    
    return redirect( 'fiche_management:sheet-detail', pk=fiche.id) 


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
    
