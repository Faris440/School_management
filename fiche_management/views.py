from django.shortcuts import render
from .forms import FinalAgentPermanentFormCollection, EnseignementsForm, FinalAgentVacataireFormCollection ,SheetSelfForm,FinalPermanentFormCollection,FinalVacataireFormCollection,SheetSelfForm,SheetFormu 
from .models import Sheet, Enseignements
from School_management import views as cviews
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.contrib import messages
from django.views.generic import TemplateView, View
from xauth.models import Nomination, User
from parameter.models import Promotion, Filiere, Niveau, Semestre,Module
from datetime import date
from notifications.models import Notification
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.db.models import Q  # Si vous en avez besoin pour des filtres
import functools

from django.conf import settings
from django.views.generic import DetailView

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from django_weasyprint.utils import django_url_fetcher

# Create your views here.



class MyDetailView(DetailView):
    model = Sheet
    template_name = 'sheet_pdf.html'

class DynamicNameView(WeasyTemplateResponseMixin, MyDetailView):
    def get_pdf_filename(self):
        sheet = self.get_object()
        return 'fiche.pdf'

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
        cond = sheet_data['gender']
        x = 0
        if cond == 'O':
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
            is_permanent = True if user.teacher_type == 'permanent' else False
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
        return getattr(self, 'success_url', reverse('fiche_management:perm_sheet_preview'))
    
    def get_collection_kwargs(self):
        kwargs =  super().get_collection_kwargs()
        if  not self.request.user.is_staff :
            kwargs['user'] = self.request.user
        return kwargs
    
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
        elif user.is_staff:
            return FinalAgentPermanentFormCollection
        return FinalVacataireFormCollection
    
    def form_collection_valid(self, form_collection):
        # Stocker les données temporairement dans la session
        sheet_data = form_collection.cleaned_data.get('sheet')
        enseignements = form_collection.cleaned_data.get('enseignement')
        print(sheet_data)
        enseignant = sheet_data.get('enseignant')
        if enseignant is None:
            enseignant = self.request.user
        promotion = sheet_data['promotion']
        date_debut = sheet_data.get('date_debut')
        date_fin = sheet_data.get('date_fin')
        cond = sheet_data.get('gender')
        print(cond)
        # Vérification des doublons dans les modules
        modules_labels = set()
        for enseignement in enseignements:
            module = enseignement['log']['module']
            if module.label in modules_labels:
                return self.form_collection_invalid(form_collection)  # Invalider le formulaire
            modules_labels.add(module.label)
        # Conversion des UUID en chaînes pour éviter les problèmes de sérialisation

        if cond == 'O':
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

                
                
                'etablissement_enseigne': sheet_data['etablissement_enseigne'],
                # is permanent
                
                'is_permanent': True,
                'volume_horaire_statuaire': sheet_data['volume_horaire_statuaire'],
                'abattement': sheet_data['abattement'],
                'motif_abattement': sheet_data['motif_abattement'],
                'v_h_obli_apres_abattement': (
                    sheet_data['volume_horaire_statuaire'] - sheet_data['abattement']
                ),
                'date_debut': {
                    'id': str(date_debut) if date_debut else None,
                    'label': str(date_debut) if date_debut else None
                },
                'date_fin': {
                    'id': str(date_fin) if date_fin else None,
                    'label': str(date_fin) if date_fin else None
                },
            }
        else :
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
            'etablissement_enseigne': sheet_data['etablissement_enseigne'],
            }

    
        self.request.session['enseignement_data'] = {}
        for enseignement in enseignements:
            enseignement = enseignement['log']
            niveau = enseignement['niveau']
            filiere = enseignement['filiere']
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
                'filiere': {
                    'id': str(filiere.id) if filiere else None,
                    'label': filiere.label
            },
                "ct_volume_horaire_confie": enseignement['ct_volume_horaire_confie'],
                "td_volume_horaire_confie": enseignement['td_volume_horaire_confie'],
                "tp_volume_horaire_confie": enseignement['tp_volume_horaire_confie'],
            }

            # Utilisation de str() pour sérialiser les UUID
            self.request.session['enseignement_data'][enseignement['code']] = ens
        if cond == 'O':
                self.success_url = reverse('fiche_management:perm_sheet_preview')          
        else :
                self.success_url = reverse('fiche_management:sheet_preview')  

        # Rediriger vers la vue de prévisualisation
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
        
        modules_labels = set()  # Utiliser un set pour détecter les doublons
        for enseignement in enseignements:
            module = enseignement['log']['module']
            if module.label in modules_labels:

                return self.form_collection_invalid(form_collection)  # Invalider le formulaire
            modules_labels.add(module.label)

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

        }

        self.request.session['enseignement_data'] = {}
        for enseignement in enseignements:
            enseignement = enseignement['log']
            filiere = enseignement['filiere']
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
                'filiere': {
                    'id': str(filiere.id) if filiere else None,
                    'label': filiere.label
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
    paginate_by = 10  # Nombre d'éléments par page

    def get_queryset(self):
        user = self.request.user

        # Vérifiez si l'utilisateur est un administrateur ou possède des permissions spécifiques
        if not user.is_staff:
            enseignements_queryset = Enseignements.objects.filter(sheet__enseignant=user)
            nomination = Nomination.objects.filter(user=user, is_desactivate=False).first()
            print(nomination)
            if nomination is None:
                return Sheet.objects.filter(
                    enseignement_sheet__in=enseignements_queryset
                ).distinct()
            
            access_vice_president = self.request.user.has_perm("xauth.vice_president")
            access_programme = self.request.user.has_perm("xauth.responsable_programme")
            access_responsable_filiere = self.request.user.has_perm("xauth.responsable_filiere")

            # Initialiser un queryset vide
            enseignements_queryset = Enseignements.objects.all()

            if access_programme:
                # Enseignements liés au département
                enseignements_queryset = Enseignements.objects.filter(
                    filiere__departement=nomination.departement
                )
            
            if access_responsable_filiere:
                # Enseignements liés à la filière
                enseignements_queryset = Enseignements.objects.filter(
                    filiere=nomination.filiere
                )
            

            # Récupérer les fiches associées
            queryset = Sheet.objects.filter(
                enseignement_sheet__in=enseignements_queryset
            ).distinct()
            return queryset

        # Par défaut, on retourne le queryset standard
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupération du queryset et application de la pagination
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')  # Récupérer la page actuelle
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            # Si la page n'est pas un entier, retourner la première page
            page_obj = paginator.page(1)
        except EmptyPage:
            # Si la page est hors limites, retourner la dernière page
            page_obj = paginator.page(paginator.num_pages)

        # Ajout des informations de pagination au contexte
        context['object_list'] = page_obj  # Les objets de la page actuelle
        context['page_obj'] = page_obj
        context['is_paginated'] = paginator.num_pages > 1  # Vérifie si la pagination est nécessaire
        context['paginator'] = paginator

        # Liens pour l'utilisateur (personnalisation spécifique à votre projet)
        app_name = "fiche_management"
        model_name = self.model._meta.model_name
        add_multi = self.request.user.has_perm(f"{app_name}.can_add_multiple_{model_name}")
        print(add_multi)
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
            print('azertyui')

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
        nomination = Nomination.objects.filter(user = user , is_desactivate = False).first()
        context['nomination'] = nomination
        context['check'] = False
        context['count_validate'] = 0
        context['count_invalidate'] = 0
        context['count_inprocess'] = 0
        context['count_validate_filiere'] = 0
        context['count_validate_programme'] = 0
        context['count_validate_vice_president'] = 0
        context["card_title"] = sheet.enseignant
        
        access_vice_president = self.request.user.has_perm("xauth.vice_president")
        access_programme = self.request.user.has_perm("xauth.responsable_programme")
        access_responsable_filiere = self.request.user.has_perm("xauth.responsable_filiere")
        print(access_responsable_filiere, "zsdefrgthyjuklk,nbvcxwqszdefghjk")
        context['access_vice_president'] = access_vice_president
        context['access_programme'] = access_programme
        context['access_responsable_filiere'] = access_responsable_filiere
        print(context['access_vice_president'],context['access_programme'],context['access_responsable_filiere'])
        enseignements = sheet.enseignement_sheet.all()

        all_enseignement = []
        for enseignement in enseignements:
            if nomination :
                if nomination.nomination_type == "filiere":
                    if enseignement.filiere == nomination.filiere:
                        all_enseignement.append(enseignement)
                elif nomination.nomination_type == "ufr":
                    if enseignement.filiere.departement == nomination.departement:
                        all_enseignement.append(enseignement)
                else:
                    all_enseignement.append(enseignement)
            else :
                all_enseignement.append(enseignement)

        context['check_in'] = False
        print(nomination)

        for enseignement in all_enseignement:
            if nomination:
                if nomination.nomination_type == "filiere" and access_responsable_filiere:
                    if enseignement.validate_by_responsable_filiere is None:
                        context['check_in'] = True
                elif nomination.nomination_type == "ufr" and access_programme:
                    if enseignement.validate_by_responsable_filiere is True and  enseignement.validate_by_responsable_programme is None:
                        context['check_in'] = True
                else:
                    if access_vice_president and enseignement.validate_by_responsable_programme is True and  enseignement.validate_by_vice_presient is None:
                        context['check_in'] = True
            else:
                context['check_in'] = False


        for enseignement in enseignements:
            
            if nomination:
                if nomination.nomination_type == "filiere":
                    if enseignement.filiere == nomination.filiere:
                        if enseignement.validate_by_responsable_filiere:
                            context['count_validate_filiere'] += 1
                        if enseignement.validate_by_vice_presient:
                            context['count_validate'] += 1
                        elif enseignement.validate_by_vice_presient is False:
                            context['count_invalidate'] += 1
                        elif enseignement.validate_by_responsable_programme is False:
                            context['count_invalidate'] += 1
                        elif enseignement.validate_by_responsable_filiere is False:
                            context['count_invalidate'] += 1
                        else:
                            context['count_inprocess'] += 1
                elif nomination.nomination_type == "ufr":

                    if enseignement.filiere.departement == nomination.departement:
                        if enseignement.validate_by_responsable_programme:
                            context['count_validate_programme'] += 1
                        if enseignement.validate_by_vice_presient:
                            context['count_validate'] += 1
                        elif enseignement.validate_by_vice_presient is False:
                            context['count_invalidate'] += 1
                        elif enseignement.validate_by_responsable_programme is False:
                            context['count_invalidate'] += 1
                        elif enseignement.validate_by_responsable_filiere is False:
                            context['count_invalidate'] += 1
                        else:
                            context['count_inprocess'] += 1
                else :
                    if enseignement.validate_by_vice_presient:
                        context['count_validate'] += 1
                    elif enseignement.validate_by_vice_presient is False:
                        context['count_invalidate'] += 1
                    elif enseignement.validate_by_responsable_programme is False:
                        context['count_invalidate'] += 1
                    elif enseignement.validate_by_responsable_filiere is False:
                        context['count_invalidate'] += 1
                    else:
                        context['count_inprocess'] += 1
            else :
                    if enseignement.validate_by_vice_presient:
                        context['count_validate'] += 1
                    elif enseignement.validate_by_vice_presient is False:
                        context['count_invalidate'] += 1
                    elif enseignement.validate_by_responsable_programme is False:
                        context['count_invalidate'] += 1
                    elif enseignement.validate_by_responsable_filiere is False:
                        context['count_invalidate'] += 1
                    else:
                        context['count_inprocess'] += 1

            context['enseignements'] = all_enseignement

        return context

    


class SheetUpdateView(cviews.CustomUpdateView):
    model = Sheet
    form_class = SheetFormu  # Spécifiez les champs que vous voulez afficher dans le formulaire

    def get_success_url(self):
        return reverse('fiche_management:sheet-list')  # Redirige vers la liste après la mise à jour

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EnseignementUpdateView(cviews.CustomUpdateView):
    model = Enseignements
    form_class = EnseignementsForm

    def get_success_url(self):
        return reverse('fiche_management:sheet-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EnseignementDeleteView(cviews.CustomDeleteView):
    model = Enseignements
    success_url = reverse_lazy('fiche_management:sheet-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SheetDeleteView(cviews.CustomDeleteView):
    model = Sheet
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
            fiche.validate_by_responsable_programme = True
            for elem in enseignements :
                elem.validate_by_responsable_programme = True
                elem.save()
        elif type == 'filiere':
            fiche.validate_by_responsable_filiere = True
            for elem in enseignements :
                elem.validate_by_responsable_filiere = True
                elem.save()
            if not fiche.is_permanent :
                fiche.validate_by_responsable_programme = True
                for elem in enseignements :
                    elem.validate_by_responsable_programme = True
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
            fiche.validate_by_responsable_programme = False
            for elem in enseignements :
                elem.validate_by_responsable_programme = False
                elem.save()
        elif type == 'filiere':
            fiche.validate_by_responsable_filiere = False
            for elem in enseignements :
                elem.validate_by_responsable_filiere = False
                elem.save()
            if not fiche.is_permanent :
                fiche.validate_by_responsable_programme = False
                for elem in enseignements :
                    elem.validate_by_responsable_programme = False
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
    access_vice_president = request.user.has_perm("xauth.vice_president")
    access_programme = request.user.has_perm("xauth.responsable_programme")
    access_responsable_filiere = request.user.has_perm("xauth.responsable_filiere")
    queryset = Sheet.objects.none()
    if access_programme:
        enseignement.validate_by_responsable_programme = True
    elif access_responsable_filiere:
        enseignement.validate_by_responsable_filiere = True
        if not enseignement.sheet.is_permanent :
            enseignement.validate_by_responsable_programme = True
    elif access_vice_president:
        enseignement.validate_by_vice_presient = True
    enseignement.save()
    messages.success(request, "La fiche a été validée avec succès !")
    print(enseignement.validate_by_responsable_filiere)
    return redirect( 'fiche_management:sheet-detail', pk=enseignement.sheet.id) 


# vue pour rejeter un enseignement

def rejeter_enseignement(request, pk):
    enseignement = get_object_or_404(Enseignements, id=pk)
    user = request.user
    access_vice_president = request.user.has_perm("xauth.vice_president")
    access_programme = request.user.has_perm("xauth.responsable_programme")
    access_responsable_filiere = request.user.has_perm("xauth.responsable_filiere")
    queryset = Sheet.objects.none()
    if request.method == "POST":
        motif_rejet = request.POST.get("motif_rejet")
            
        if access_programme:
            enseignement.validate_by_responsable_programme = False
        elif access_responsable_filiere:
            enseignement.validate_by_responsable_filiere = False
        elif access_vice_president:
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
                is_permanent=sheet_data.get('is_permanent', False)
            )
            
            # Créer les enseignements associés
            for enseignement in enseignement_data:
                Enseignements.objects.create(
                    sheet=sheet,
                    code=enseignement['code'],
                    niveau=enseignement['niveau'],
                    filiere = enseignement['filiere'],
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
        if not sheet_data or not enseignement_data:
            messages.error(request, "Aucune donnée à prévisualiser.")
            return redirect('fiche_management:sheet_create')
        return_url = request.META.get('HTTP_REFERER', '/')
        # Afficher le récapitulatif
        enseignant = get_object_or_404(User, id = sheet_data['enseignant']['id'])

        total_ct = sum(item['ct_volume_horaire_confie'] for item in enseignement_data.values())
        total_td = sum(item['td_volume_horaire_confie'] for item in enseignement_data.values())
        total_tp = sum(item['tp_volume_horaire_confie'] for item in enseignement_data.values())

        print(sheet_data)

        today = date.today()
        context = {
            'sheet_data': sheet_data,
            'enseignement_data': enseignement_data,
            'total_td': total_td,
            'total_tp': total_tp,
            'total_ct': total_ct,
            'return_url' : return_url,
            'today': today,
            'grade' : enseignant.grade

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
        print(enseignement_data)
        enseignant = get_object_or_404(User, id = sheet_data['enseignant']['id'])
        promotion = get_object_or_404(Promotion, id = sheet_data['promotion']['id'])
        sheet = Sheet.objects.create(
            enseignant=enseignant,
            promotion=promotion,
            is_permanent=False,
        )

        index = 1
        keys = list(enseignement_data.keys())  # Liste ordonnée des clés
        for idx, (key, value) in enumerate(enseignement_data.items()):
            enseignement = value
            niveau = get_object_or_404(Niveau, id = enseignement['niveau']['id'])
            semestre = get_object_or_404(Semestre, id = enseignement['semestre']['id'])
            filiere = get_object_or_404(Filiere, id = enseignement['filiere']['id'])
            module = get_object_or_404(Module, id = enseignement['module']['id'])

            Enseignements.objects.create(
                code=enseignement['code'],
                sheet=sheet,
                niveau=niveau,
                filiere = filiere,
                semestre=semestre,
                module=module,
                ct_volume_horaire_confie=enseignement['ct_volume_horaire_confie'],
                td_volume_horaire_confie=enseignement['td_volume_horaire_confie'],
                tp_volume_horaire_confie=enseignement['tp_volume_horaire_confie'],
            )

        messages.success(request, "Le dossier a été soumis avec succès!")
        return redirect('fiche_management:sheet-list')
    


class SheetPermanantPreviewView(View):
    template_name = 'perm_sheet_preview.html'

    def get(self, request):
        # Récupérer les données de la session
        sheet_data = request.session.get('sheet_data')
        enseignement_data = request.session.get('enseignement_data')
        if not sheet_data or not enseignement_data:
            messages.error(request, "Aucune donnée à prévisualiser.")
            return redirect('fiche_management:sheet_create')

        return_url = request.META.get('HTTP_REFERER', '/')
        print(sheet_data)
        enseignant = get_object_or_404(User, id=sheet_data['enseignant']['id'])

        # Calculer les totaux pour les volumes horaires
        total_ct = sum(item['ct_volume_horaire_confie'] for item in enseignement_data.values())
        total_td = sum(item['td_volume_horaire_confie'] for item in enseignement_data.values())
        total_tp = sum(item['tp_volume_horaire_confie'] for item in enseignement_data.values())

        # Calculer les champs spécifiques aux permanents
        v_h_obli_apres_abattement = sheet_data['v_h_obli_apres_abattement']

        today = date.today()
        context = {
            'sheet_data': sheet_data,
            'enseignement_data': enseignement_data,
            'total_td': total_td,
            'total_tp': total_tp,
            'total_ct': total_ct,
            'v_h_obli_apres_abattement': v_h_obli_apres_abattement,
            'return_url': return_url,
            'today': today,
            'grade': enseignant.grade,
            'is_permanent': True,
            'etablissement_enseigne': sheet_data['etablissement_enseigne'],
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
        enseignant = get_object_or_404(User, id=sheet_data['enseignant']['id'])
        promotion = get_object_or_404(Promotion, id=sheet_data['promotion']['id'])

        sheet = Sheet.objects.create(
            enseignant=enseignant,
            promotion=promotion,
            is_permanent=True,
            volume_horaire_statuaire=sheet_data['volume_horaire_statuaire'],
            abattement=sheet_data['abattement'],
            motif_abattement=sheet_data['motif_abattement'],
            v_h_obli_apres_abattement=sheet_data['v_h_obli_apres_abattement'],
            etablissement_enseigne=sheet_data['etablissement_enseigne'],
        )

        for key, enseignement in enseignement_data.items():
            filiere = get_object_or_404(Filiere, id=enseignement['filiere']['id'])
            niveau = get_object_or_404(Niveau, id=enseignement['niveau']['id'])
            semestre = get_object_or_404(Semestre, id=enseignement['semestre']['id'])
            module = get_object_or_404(Module, id=enseignement['module']['id'])

            Enseignements.objects.create(
                code=enseignement['code'],
                sheet=sheet,
                niveau=niveau,
                filiere = filiere,
                semestre=semestre,
                module=module,
                ct_volume_horaire_confie=enseignement['ct_volume_horaire_confie'],
                td_volume_horaire_confie=enseignement['td_volume_horaire_confie'],
                tp_volume_horaire_confie=enseignement['tp_volume_horaire_confie'],
            )

        messages.success(request, "Le dossier permanent a été soumis avec succès!")
        return redirect('fiche_management:sheet-list')


# class NotificationsListView(ListView):
#     """
#     Vue pour afficher les notifications non lues d'un utilisateur.
#     Utilise une vue générique ListView pour une meilleure structure.
#     """
#     model = Notification
#     template_name = 'notifications_list.html'
#     context_object_name = 'notifications'
#     paginate_by = 10  # Nombre de notifications par page

#     def get_queryset(self):
#         """
#         Récupère les notifications non lues pour l'utilisateur connecté.
#         """
#         return self.request.user.notifications.unread()

#     def get_context_data(self, **kwargs):
#         """
#         Ajoute des informations contextuelles supplémentaires, comme le nombre total de notifications.
#         """
#         context = super().get_context_data(**kwargs)
#         context['total_notifications'] = self.request.user.notifications.count()
#         context['unread_notifications'] = self.request.user.notifications.unread().count()
#         return context





def batch_validate_or_reject(request):
    if request.method == "POST":
        enseignement_ids = request.POST.getlist("enseignement_ids")
        action = request.POST.get("action")
        reasons = request.POST.get("reasons", {})
        print(reasons)

        if not enseignement_ids:
            messages.error(request, "Veuillez sélectionner au moins un enseignement.")
            return redirect(request.META.get('HTTP_REFERER'))

        enseignements = get_list_or_404(Enseignements, id__in=enseignement_ids)
        user = request.user
        access_vice_president = request.user.has_perm("xauth.vice_president")
        access_programme = request.user.has_perm("xauth.responsable_programme")
        access_responsable_filiere = request.user.has_perm("xauth.responsable_filiere")

        if action == "validate":
            for enseignement in enseignements:
                if access_programme:
                    enseignement.validate_by_responsable_programme = True
                elif access_responsable_filiere:
                    enseignement.validate_by_responsable_filiere = True
                    if not enseignement.sheet.is_permanent :
                        enseignement.validate_by_responsable_programme = True
                elif access_vice_president:
                    enseignement.validate_by_vice_presient = True
                    enseignement.is_validated = True
                enseignement.save()
            messages.success(request, f"{len(enseignements)} enseignement(s) validé(s) avec succès.")
        elif action == "reject":
            for enseignement in enseignements:
                motif = request.POST.get(f"reasons[{enseignement.id}]")
                if access_programme:
                    enseignement.validate_by_responsable_programme = False
                elif access_responsable_filiere:
                    enseignement.validate_by_responsable_filiere = False
                    if not enseignement.sheet.is_permanent :
                        enseignement.validate_by_responsable_programme = False
                elif access_vice_president:
                    enseignement.validate_by_vice_presient = False
                enseignement.motif_de_rejet = motif
                enseignement.is_validated = False
                enseignement.save()
            messages.success(request, f"{len(enseignements)} enseignement(s) rejeté(s) avec succès.")
        else:
            messages.error(request, "Action non reconnue.")

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "Méthode non autorisée.")
        return redirect("fiche_management:sheet-list")
    


# from django.views.generic import ListView

# from django.core.paginator import EmptyPage, PageNotAnInteger

# class SheetListView(ListView):
#     model = Sheet
#     template_name = '.html'
#     context_object_name = 'object_list'
#     paginate_by = 10

#     def get_queryset(self):
#         queryset = Sheet.objects.all()
#         query = self.request.GET.get('query')
#         if query:
#             queryset = queryset.filter(nom__icontains=query)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         page = self.request.GET.get('page')
#         try:
#             page = int(page) if page else 1
#             if page < 1:
#                 page = 1
#         except ValueError:
#             page = 1
#         context['page_obj'] = self.paginate_queryset(self.get_queryset(), self.paginate_by)
#         return context
