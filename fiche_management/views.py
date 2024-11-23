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
                promotion = sheet_data['promotion'],
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
                promotion = sheet_data['promotion'],
                date_debut = sheet_data['date_debut'],
                date_fin = sheet_data['date_fin'],
                etablissement_enseigne = sheet_data['etablissement_enseigne'],
                is_permanent = False,
                filiere=sheet_data['filiere'],
                )
        elif type == '0' :
            sheet = Sheet.objects.create(
            enseignant = sheet_data['enseignant'],
            promotion = sheet_data['promotion'],
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
            promotion = sheet_data['promotion'],
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
            promotion = sheet_data['promotion'],
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
        return reverse('fiche_management:sheet_preview')

    def form_collection_valid(self, form_collection):
        # Stocker les données temporairement dans la session
        sheet_data = form_collection.cleaned_data.get('sheet')
        enseignements = form_collection.cleaned_data.get('enseignement')
        enseignant = sheet_data['enseignant']
        promotion = sheet_data['promotion']
        filiere = sheet_data['filiere']

        # Conversion des UUID en chaînes pour éviter l'erreur
        self.request.session['sheet_data'] = {
            'enseignant': {
                'id': str(enseignant.id) if enseignant else None,
                'lastname': f"{enseignant.last_name}",
                'firstname': f"{enseignant.first_name}"
            },
            'promotion': {
                'id': str(promotion.id) if promotion else None,
                'label': promotion.name
            },
            'filiere': {
                'id': str(filiere.id) if filiere else None,
                'label': filiere.label
            }
        }

        self.request.session['enseignement_data'] = {}
        for enseignement in enseignements:
            enseignement = enseignement['log']
            niveau = enseignement['niveau']
            semestre = enseignement['semestre']
            module = enseignement['module']
            ens = {
                "code": enseignement['code'],
                "niveau": {
                    "id": str(niveau.id),
                    "label": niveau.label
                },
                "semestre": {
                    "id": str(semestre.id),
                    "label": semestre.label
                },
                "module": {
                    "id": str(module.id),
                    "label": module.label
                },
                "ct_volume_horaire_confie": enseignement['ct_volume_horaire_confie'],
                "td_volume_horaire_confie": enseignement['td_volume_horaire_confie'],
                "tp_volume_horaire_confie": enseignement['tp_volume_horaire_confie'],
            }

            # Utilisation de str() pour sérialiser les UUID
            self.request.session['enseignement_data'][enseignement['code']] = ens

    # Rediriger vers la vue de prévisualisation
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
        sheet = self.get_object()
        context['nomination'] = Nomination.objects.filter(user = user , is_desactivate = False).first()
        context['count_validate'] = 0
        context['count_invalidate'] = 0
        context['count_inprocess'] = 0
        enseignements = sheet.enseignement_sheet.all()
        for enseignement in enseignements:
            if enseignement.validate_by_vice_presient:
                context['count_validate'] += 1
            elif enseignement.validate_by_vice_presient is False:
                context['count_invalidate'] += 1
            elif enseignement.validate_by_responsable_ufr is False:
                context['count_invalidate'] += 1
            elif enseignement.validate_by_responsable_filiere is False:
                context['count_invalidate'] += 1
            else:
                context['count_inprocess'] += 1


        print()
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
        enseignements = fiche.enseignement_sheet.all()
        if type == 'ufr':
            fiche.validate_by_responsable_ufr = True
            for elem in enseignements :
                elem.validate_by_responsable_ufr = True
                elem.save()
        elif type == 'filiere':
            fiche.validate_by_responsable_filiere = True
            for elem in enseignements :
                elem.validate_by_responsable_filiere = True
                elem.save()
            if not fiche.is_permanent :
                fiche.validate_by_responsable_ufr = True
                for elem in enseignements :
                    elem.validate_by_responsable_ufr = True
                    elem.save()
        elif type == 'vise-president':
            fiche.validate_by_vice_presient = True
            for elem in enseignements :
                elem.validate_by_vice_presient = True
                elem.save()
        
        fiche.save()
        messages.success(request, "La fiche a été validée avec succès !")

    return redirect( 'fiche_management:sheet-detail', pk=fiche.id) 



def rejeter_fiche(request, pk):
    fiche = get_object_or_404(Sheet, id=pk)
    user = request.user
    nomination = Nomination.objects.filter(user = user , is_desactivate = False).first()
    type = nomination.nomination_type
    if request.method == "POST":
        print('okjk')
        motif_rejet = request.POST.get("motif_rejet")
        enseignements = fiche.enseignement_sheet.all()
        if type == 'ufr':
            fiche.validate_by_responsable_ufr = False
            for elem in enseignements :
                elem.validate_by_responsable_ufr = False
                elem.save()
        elif type == 'filiere':
            fiche.validate_by_responsable_filiere = False
            for elem in enseignements :
                elem.validate_by_responsable_filiere = False
                elem.save()
            if not fiche.is_permanent :
                fiche.validate_by_responsable_ufr = False
                for elem in enseignements :
                    elem.validate_by_responsable_ufr = False
                    elem.save()
        elif type == 'vise-president':
            fiche.validate_by_vice_presient = False
            for elem in enseignements :
                elem.validate_by_vice_presient = False
                elem.save()
        fiche.motif_de_rejet = motif_rejet
        fiche.save()
        messages.success(request, "La fiche a été rejetée avec le motif indiqué.")
        return redirect( 'fiche_management:sheet-detail', pk=fiche.id) 
    else:
            messages.error(request, "Veuillez fournir un motif pour le rejet.")
    
    return redirect( 'fiche_management:sheet-detail', pk=fiche.id) 


def valider_enseignement(request, pk):
    enseignement = get_object_or_404(Enseignements, id=pk)
    user = request.user
    nomination = Nomination.objects.filter(user = user , is_desactivate = False).first()
    type = nomination.nomination_type
    if type == 'ufr':
        enseignement.validate_by_responsable_ufr = True
    elif type == 'filiere':
        enseignement.validate_by_responsable_filiere = True
        if not enseignement.sheet.is_permanent :
            enseignement.validate_by_responsable_ufr = True
    elif type == 'vise-president':
        enseignement.validate_by_vice_presient = True
    enseignement.save()
    messages.success(request, "La fiche a été validée avec succès !")
    print(enseignement.validate_by_responsable_filiere)
    return redirect( 'fiche_management:sheet-detail', pk=enseignement.sheet.id) 


# vue pour rejeter un enseignement

def rejeter_enseignement(request, pk):
    enseignement = get_object_or_404(Enseignements, id=pk)
    user = request.user
    nomination = Nomination.objects.filter(user = user , is_desactivate = False).first()
    type = nomination.nomination_type
    if request.method == "POST":
        motif_rejet = request.POST.get("motif_rejet")
            
        if type == 'ufr':
            enseignement.validate_by_responsable_ufr = False
        elif type == 'filiere':
            enseignement.validate_by_responsable_filiere = False
        elif type == 'vise-president':
            enseignement.validate_by_vice_presient = False
        else:
            messages.error(request, "Veuillez fournir un motif pour le rejet.")
        enseignement.motif_de_rejet = motif_rejet
        enseignement.save()
        messages.success(request, "L'enseignement a été rejeté avec le motif indiqué.")
    
    return redirect( 'fiche_management:sheet-detail', pk=enseignement.sheet.id) 



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
    

class EnseignemtUpdateView(cviews.CustomUpdateView):
    model = Enseignements
    form_class = EnseignementsForm

    def get_success_url(self):
        ob = self.get_object()
        return reverse('fiche_management:sheet-detail', kwargs={'pk' : ob.sheet.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


class SheetPreviewView(View):
    template_name = 'sheet_preview.html'

    def get(self, request):
        # Récupérer les données de la session
        sheet_data = request.session.get('sheet_data')
        enseignement_data = request.session.get('enseignement_data')
        print(enseignement_data)
        if not sheet_data or not enseignement_data:
            messages.error(request, "Aucune donnée à prévisualiser.")
            return redirect('fiche_management:sheet_create')

        # Afficher le récapitulatif
        context = {
            'sheet_data': sheet_data,
            'enseignement_data': enseignement_data,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # Soumission finale des données
        sheet_data = request.session.pop('sheet_data', None)
        enseignement_data = request.session.pop('enseignement_data', None)

        if not sheet_data or not enseignement_data:
            messages.error(request, "Erreur lors de la soumission.")
            return redirect('fiche_management:sheet_create')

        # Enregistrer les données dans la base de données
        sheet = Sheet.objects.create(
            enseignant=sheet_data['enseignant'],
            promotion=sheet_data['promotion'],
            etablissement_enseigne=sheet_data['etablissement_enseigne'],
            filiere=sheet_data['filiere'],
            is_permanent=False,
        )

        for ens in enseignement_data:
            enseignement = ens['log']
            Enseignements.objects.create(
                code=enseignement['code'],
                sheet=sheet,
                niveau=enseignement['niveau'],
                semestre=enseignement['semestre'],
                module=enseignement['module'],
                ct_volume_horaire_confie=enseignement['ct_volume_horaire_confie'],
                td_volume_horaire_confie=enseignement['td_volume_horaire_confie'],
                tp_volume_horaire_confie=enseignement['tp_volume_horaire_confie'],
            )

        messages.success(request, "Le dossier a été soumis avec succès!")
        return redirect('fiche_management:sheet_success')
