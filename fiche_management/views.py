from django.shortcuts import render
from .forms import FinalAgentPermanentFormCollection, EnseignementsForm, FinalAgentVacataireFormCollection ,SheetSelfForm,FinalPermanentFormCollection,FinalVacataireFormCollection,SheetSelfForm,SheetFormu 
from .models import Sheet, Enseignements
from School_management import views as cviews
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import TemplateView, View
from xauth.models import Nomination
# Create your views here.

class SheetCreateView(cviews.CustomFormCollectionView):
    model = Sheet
    name = "sheet"
    
    # Redirige vers la page de prévisualisation
    def form_collection_valid(self, form_collection):
        # Sérialiser les données pour le contexte
        context = {
            'sheet_data': form_collection.cleaned_data['sheet'],
            'enseignement_data': form_collection.cleaned_data.get('enseignement', []),
        }
        # Stocke les données dans la session pour utilisation dans la vue de prévisualisation
        self.request.session['sheet_preview_data'] = context
        return redirect('fiche_management:sheet-preview')

    def get_collection_class(self):
        user = self.request.user
        type = self.request.GET.get('for')
        self.type = type
        app_name = "fiche_management"
        model_name = self.model._meta.model_name
        add_multi =self.request.user.has_perm(f"{app_name}.can_add_multiple_{model_name}")
        if not user.is_staff and not add_multi:
            if user.teacher_type == 'permanent':
                return FinalPermanentFormCollection
            elif user.teacher_type == 'vacataire':
                return FinalVacataireFormCollection
        elif add_multi and type == '0':
            return FinalAgentPermanentFormCollection
        elif add_multi and type == '1':
            return FinalAgentVacataireFormCollection
        return FinalVacataireFormCollection
    
    def get_success_url(self):
        return reverse('fiche_management:sheet-list')
    
    def form_collection_valid(self, form_collection):
        type = self.kwargs.get("type")
        sheet_data = form_collection.cleaned_data['sheet']
        enseignement_data = form_collection.cleaned_data.get('enseignement')
        user = self.request.user
        sheet = None
        x = sheet_data['volume_horaire_statuaire'] - sheet_data['abattement']
        if not user.is_staff :
            if user.teacher_type == 'permanent':
                sheet = Sheet.objects.create(
                enseignant = user,
                date_debut = sheet_data['date_debut'],
                date_fin = sheet_data['date_fin'],
                etablissement_enseigne = sheet_data['etablissement_enseigne'],
                abattement = sheet_data['abattement'],
                volume_horaire_statuaire = sheet_data['volume_horaire_statuaire'],
                motif_abattement = sheet_data['motif_abattement'],
                v_h_obli_apres_abattement = x,
                is_permanent = True,
                filiere=sheet_data['filiere'],

                )
            elif user.teacher_type == 'vacataire':
                sheet = Sheet.objects.create(
                enseignant = user,
                date_debut = sheet_data['date_debut'],
                date_fin = sheet_data['date_fin'],
                etablissement_enseigne = sheet_data['etablissement_enseigne'],
                is_permanent = False,
                filiere=sheet_data['filiere'],
                )
        elif type == '0' :
            sheet = Sheet.objects.create(
            enseignant = sheet_data['enseignant'],
            date_debut = sheet_data['date_debut'],
            date_fin = sheet_data['date_fin'],
            etablissement_enseigne = sheet_data['etablissement_enseigne'],
            abattement = sheet_data['abattement'],
            volume_horaire_statuaire = sheet_data['volume_horaire_statuaire'],
            motif_abattement = sheet_data['motif_abattement'],
            v_h_obli_apres_abattement = x,
            filiere=sheet_data['filiere'],
            )
        elif type == '1' :
            sheet = Sheet.objects.create(
            enseignant = sheet_data['enseignant'],
            date_debut = sheet_data['date_debut'],
            date_fin = sheet_data['date_fin'],
            etablissement_enseigne = sheet_data['etablissement_enseigne'],
            filiere=sheet_data['filiere'],
            )

        for ens in enseignement_data :
            enseignement = ens['log']
            enseignements = Enseignements.objects.create(
                code = enseignement['code'],
                sheet = sheet,
                niveau = enseignement['niveau'],
                semestre = enseignement['semestre'],
                module = enseignement['module'],
                
                ct_volume_horaire_confie = enseignement['ct_volume_horaire_confie'],
                ct_volume_horaire_efectue = enseignement['ct_volume_horaire_efectue'],
                td_volume_horaire_confie = enseignement['td_volume_horaire_confie'],
                td_volume_horaire_efectue = enseignement['td_volume_horaire_efectue'],
                tp_volume_horaire_confie = enseignement['tp_volume_horaire_confie'],
                tp_volume_horaire_efectue = enseignement['tp_volume_horaire_efectue'],
            )
        
        messages.success(self.request, f'Le dossier a été enregistré avec succès!')
        return JsonResponse({'success_url': self.get_success_url()})
    

class SheetPermananteCreateByAgentView(cviews.CustomFormCollectionView):
    model = Sheet
    name = "sheet"
    collection_class = FinalAgentPermanentFormCollection
    
    def get_success_url(self):
        return reverse('fiche_management:sheet-list')
    
    def form_collection_valid(self, form_collection):
        type = self.kwargs.get("type")
        sheet_data = form_collection.cleaned_data.get('sheet')
        enseignement_data = form_collection.cleaned_data.get('enseignement')
        x = sheet_data['volume_horaire_statuaire'] - sheet_data['abattement']
        sheet = Sheet.objects.create(
            enseignant = sheet_data['enseignant'],
            date_debut = sheet_data['date_debut'],
            date_fin = sheet_data['date_fin'],
            etablissement_enseigne = sheet_data['etablissement_enseigne'],
            abattement = sheet_data['abattement'],
            volume_horaire_statuaire = sheet_data['volume_horaire_statuaire'],
            motif_abattement = sheet_data['motif_abattement'],
            v_h_obli_apres_abattement = x,
            is_permanent = True,
            filiere=sheet_data['filiere'],
            )

        for ens in enseignement_data :
            enseignement = ens['log']
            enseignements = Enseignements.objects.create(
                code = enseignement['code'],
                sheet = sheet,
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
    


class SheetVacataireCreateByAgentView(cviews.CustomFormCollectionView):
    model = Sheet
    name = "sheet"
    collection_class = FinalAgentVacataireFormCollection
    
    def get_success_url(self):
        return reverse('fiche_management:sheet-list')
    
    def form_collection_valid(self, form_collection):
        sheet_data = form_collection.cleaned_data.get('sheet')
        enseignement_data = form_collection.cleaned_data.get('enseignement')
        
        sheet = Sheet.objects.create(
            enseignant = sheet_data['enseignant'],
            date_debut = sheet_data['date_debut'],
            date_fin = sheet_data['date_fin'],
            etablissement_enseigne = sheet_data['etablissement_enseigne'],
            filiere=sheet_data['filiere'],
            is_permanent = False,
        )

        for ens in enseignement_data :
            enseignement = ens['log']
            enseignements = Enseignements.objects.create(
                code = enseignement['code'],
                sheet = sheet,
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
            nomination = Nomination.objects.filter(user = user , is_desactivate = False).first()
            print(nomination)
            if nomination :
                queryset = Sheet.objects.none()

                if nomination.ufr is not None:
                    print(1, nomination.ufr)
                    queryset |= Sheet.objects.filter(filiere__departement__ufr=nomination.ufr)
                    return queryset
                if nomination.departement is not None:
                    print(2)
                    queryset |= Sheet.objects.filter(filiere__departement=nomination.departement)
                    return queryset
                if nomination.filiere is not None:
                    queryset |= Sheet.objects.filter(filiere=nomination.filiere)
                    return queryset
                if nomination.nomination_type == 'vise-president':
                    queryset |= Sheet.objects.all()
                    return queryset
            return Sheet.objects.filter(enseignant = user)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        app_name = "fiche_management"
        model_name = self.model._meta.model_name
        add_multi =self.request.user.has_perm(f"{app_name}.can_add_multiple_{model_name}")
        context["links"] = [
                {
                    "label": "Fiche de Permanant",
                    "url": reverse_lazy("fiche_management:sheet-permanent-create", kwargs={"type": '0'})
                    + "?for=0",
                },
                {
                    "label": "Fiche de vacataire",
                    "url": reverse_lazy("fiche_management:sheet-vacataire-create", kwargs={"type": '1'})
                    + "?for=1",
                },
            ]
        if add_multi:
            context["multi_add"] = True
        return context


class SheetDetailView(cviews.CustomDetailView):
    model = Sheet
    template_name = "detail-sheet.html"  # Remplacez par le chemin de votre template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_name = "fiche_management"
        model_name = self.model._meta.model_name
        context["validate"] =self.request.user.has_perm(f"{app_name}.can_valide_{model_name}")
        context["invalidate"] =self.request.user.has_perm(f"{app_name}.can_invalide_{model_name}")
        user = self.request.user
        context['nomination'] = Nomination.objects.filter(user = user , is_desactivate = False).first()
        print(user, context['nomination'])
        return context
    


class SheetUpdateView(cviews.CustomUpdateView):
    model = Sheet
    form_class = SheetFormu  # Spécifiez les champs que vous voulez afficher dans le formulaire

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
    
def valider_fiche(request, pk):
    fiche = get_object_or_404(Sheet, id=pk)
    user = request.user
    nomination = Nomination.objects.filter(user = user , is_desactivate = False).first()
    type = nomination.nomination_type
    if fiche.is_validated:
        messages.warning(request, "Cette fiche a déjà été validée.")
    else:
        if type == 'ufr':
            fiche.validate_by_responsable_ufr = True
        elif type == 'filiere':
            fiche.validate_by_responsable_filiere = True
            if not fiche.is_permanent :
                fiche.validate_by_responsable_ufr = True
        elif type == 'vise-president':
            fiche.validate_by_vice_presient = True
        enseignements = Enseignements.objects.filter( sheet = fiche )

        for elem in enseignements :
            elem.is_validated = True
            elem.save()
        
        fiche.save()
        messages.success(request, "La fiche a été validée avec succès !")

    return redirect( 'fiche_management:sheet-detail', pk=fiche.id) 

def valider_enseignement(request, pk):
    enseignement = get_object_or_404(Enseignements, id=pk)
    user = request.user
    nomination = Nomination.objects.filter(user = user , is_desactivate = False).first()
    type = nomination.nomination_type
    if enseignement.is_validated:
        messages.warning(request, "Cette fiche a déjà été validée.")
    else:
        if type == 'ufr':
            enseignement.validate_by_responsable_ufr = True
        elif type == 'filiere':
            enseignement.validate_by_responsable_filiere = True
            if not enseignement.is_permanent :
                enseignement.validate_by_responsable_ufr = True
        elif type == 'vise-president':
            enseignement.validate_by_vice_presient = True
        enseignement.save()
        messages.success(request, "La fiche a été validée avec succès !")

    return redirect( 'fiche_management:sheet-detail', pk=enseignement.id) 


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


class SheetPreviewView(TemplateView):
    template_name = "sheet_preview.html"

    def post(self, request, *args, **kwargs):
        # Récupère les données soumises par le formulaire
        form_data = request.POST.dict()
        form_collection = FinalAgentPermanentFormCollection(form_data)

        # Vérifie la validité des données du formulaire
        if form_collection.is_valid():
            context = {
                'sheet_data': form_collection.cleaned_data['sheet'],
                'enseignement_data': form_collection.cleaned_data.get('enseignement', []),
            }
            return render(request, self.template_name, context)
        else:
            return render(request, "form_template.html", {"form_collection": form_collection})



class SheetConfirmView(View):
    def post(self, request, *args, **kwargs):
        # Récupère les données de prévisualisation de la session
        sheet_preview_data = request.session.get('sheet_preview_data')
        
        if sheet_preview_data:
            sheet_data = sheet_preview_data['sheet_data']
            enseignement_data = sheet_preview_data['enseignement_data']
            
            # Créer la fiche
            sheet = Sheet.objects.create(
                enseignant=request.user,
                date_debut=sheet_data['date_debut'],
                date_fin=sheet_data['date_fin'],
                etablissement_enseigne=sheet_data['etablissement_enseigne'],
                filiere=sheet_data['filiere'],
                is_permanent=sheet_data.get('is_permanent', False)
            )
            
            # Créer les enseignements associés
            for enseignement in enseignement_data:
                Enseignements.objects.create(
                    sheet=sheet,
                    code=enseignement['code'],
                    niveau=enseignement['niveau'],
                    semestre=enseignement['semestre'],
                    module=enseignement['module'],
                    ct_volume_horaire_confie=enseignement['ct_volume_horaire_confie'],
                    td_volume_horaire_confie=enseignement['td_volume_horaire_confie'],
                    tp_volume_horaire_confie=enseignement['tp_volume_horaire_confie'],
                    ct_volume_horaire_efectue=enseignement['ct_volume_horaire_efectue'],
                    td_volume_horaire_efectue=enseignement['td_volume_horaire_efectue'],
                    tp_volume_horaire_efectue=enseignement['tp_volume_horaire_efectue']
                )
            
            messages.success(request, "Fiche créée avec succès!")
            # Supprime les données de la session pour éviter la duplication
            del request.session['sheet_preview_data']
            
            return redirect('fiche_management:sheet-list')
        else:
            messages.error(request, "Erreur: données de prévisualisation manquantes.")
            return redirect('fiche_management:sheet-create')

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
    

class EnseignemtUpdateView(cviews.CustomUpdateView):
    model = Enseignements
    form_class = EnseignementsForm

    def get_success_url(self):
        ob = self.get_object()
        return reverse('fiche_management:sheet-detail', kwargs={'pk' : ob.sheet.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context