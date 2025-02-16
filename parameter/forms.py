from django import forms
from .models import MailContent, UniteDeRecherche, Departement, Filiere, UE, Module, Semestre,Niveau,Promotion,Annee_univ,Volume_horaire,Credit, Grade
from django.forms.models import ModelChoiceField , ModelMultipleChoiceField 
from formset.renderers.bootstrap import FormRenderer
from formset.widgets import (
    Selectize,
    SelectizeMultiple,
    DualSortableSelector,
    DualSelector,
)
from formset.collection import FormMixin
from formset.richtext.widgets import RichTextarea
from django.utils.safestring import mark_safe
from School_management.constants import control_elements , TEXTAREA
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.forms import fields, widgets




default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )

class UniteDeRechercheForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
  
    class Meta:
        model = UniteDeRecherche
        fields = ['code', 'label', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'Unité de Recherche'}),
            'description': CKEditorWidget(),  # Utilisation de CKEditorWidget
            }

class DepartementForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
    class Meta:
        model = Departement
        fields = ['code', 'label', 'ufr','description', ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du département'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'unite_de_recherche': forms.Select(attrs={'class': 'form-control'}),
        }


class FiliereForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
    class Meta:
        model = Filiere
        fields = ['code', 'departement','label', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la filière'}),
            'departement': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez un département",
            ),
        }
        
        

class NiveauForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
    
    class Meta:
        model = Niveau
        fields = ['code', 'label','description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du niveau'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }
    

class SemestreForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
    class Meta:
        model = Semestre
        fields = ['code', 'label', 'niveau','description', ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du département'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'niveau': forms.Select(attrs={'class': 'form-control'}),
        }


class UEForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
    class Meta:
        model = UE
        fields = ['code', 'label', 'description','filiere', 'niveau','semestre']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'UE'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'ufr': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez une UFR",
            ),
            'departement': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez une filière",
                filter_by={"UniteDeRecherche": "UniteDeRecherche__id"},  # Liaison au département sélectionné
            ),
            'filiere': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez une filière",
                filter_by={"departement": "departement__id"},  # Liaison au département sélectionné
            ),
            'niveau': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez un niveau",
            ),
            'semestre': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez un semestre",
                filter_by={"niveau": "niveau__id"},
            ),
           
        }

class ModuleForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )

    # Cases à cocher pour activer les champs
    a_cours_theorique = forms.BooleanField(
        label="Cours théorique pour ce module ?",
        required=False,
        initial=False  # La case est décochée par défaut
    )

    cours_theorique = forms.IntegerField(
        label='Nombre d\'heures cours théorique',
        widget=forms.NumberInput(attrs={'df-disable': ".a_cours_theorique==''"}),
        required=False
    )

    a_travaux_diriges = forms.BooleanField(
        label="Travaux dirigés pour ce module ?",
        required=False,
        initial=False  # La case est décochée par défaut
    )

    travaux_diriges = forms.IntegerField(
        label='Nombre d\'heures travaux dirigés prévues',
        widget=forms.NumberInput(attrs={'df-disable': ".a_travaux_diriges==''"}),
        required=False
    )

    a_travaux_pratiques = forms.BooleanField(
        label="Travaux pratiques pour ce module ?",
        required=False,
        initial=False  # La case est décochée par défaut
    )

    travaux_pratiques = forms.IntegerField(
        label='Nombre d\'heures travaux pratiques prévues',
        widget=forms.NumberInput(attrs={'df-disable': ".a_travaux_pratiques==''"}),
        required=False
    )

    class Meta:
        model = Module
        fields = [
            'code',
            'label',
            'description',
            'filiere',
            'ue',
            'volume_horaire',
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du module'}),
            'description': RichTextarea(),

            'filiere': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez une filière",
            ),
            'ue': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez une unité d'enseignement",
                filter_by={"filiere" : "filiere__id"},
            ),
            'volume_horaire': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez le volume horaire",
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Vérifier si les champs sont activés et valider la somme
        a_cours_theorique = cleaned_data.get("a_cours_theorique")
        cours_theorique = cleaned_data.get("cours_theorique", 0)
        
        a_travaux_diriges = cleaned_data.get("a_travaux_diriges")
        travaux_diriges = cleaned_data.get("travaux_diriges", 0)
        
        a_travaux_pratiques = cleaned_data.get("a_travaux_pratiques")
        travaux_pratiques = cleaned_data.get("travaux_pratiques", 0)
        
        # Calculer la somme des volumes horaires
        total_volume_horaire = 0
        
        if a_cours_theorique:
            total_volume_horaire += cours_theorique
        if a_travaux_diriges:
            total_volume_horaire += travaux_diriges
        if a_travaux_pratiques:
            total_volume_horaire += travaux_pratiques
        
        # Vérifier si le volume horaire du module correspond à la somme des heures
        volume_horaire = cleaned_data.get("volume_horaire")
        
        if volume_horaire and volume_horaire.heures != total_volume_horaire:
            raise ValidationError("Le volume horaire doit être égal à la somme des heures des cours théoriques, travaux dirigés et travaux pratiques.")
        
        return cleaned_data
    
class CustomModelForm(forms.ModelForm):
    default_renderer = default_renderer
    # submit = submit
    # reload = reload
    # reset = reset

    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        for name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span class='text-danger h3'>*</span>")

class ContentForm(CustomModelForm):
    initial_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={"*": "mt-4 mb-4 col-md-12"},
    )

    def _init_(self, **kwargs):
        super()._init_(**kwargs)

        for name, field in self.fields.items():
            if isinstance(field, forms.CharField):
                field.widget = RichTextarea(
                    control_elements=control_elements, attrs=TEXTAREA
                )

class MailContentForm(ContentForm):
    class Meta:
        model = MailContent
        exclude = ["is_removed"]



class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['name','filiere','start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Exemple : 2024-2025',
            }),
            'filiere': SelectizeMultiple(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez une filière",
            ),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'name': "Promotion",
            'start_date': "Date de Début",
            'end_date': "Date de Fin",
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if Promotion.objects.filter(code=code).exists():
            raise ValidationError("Ce code est déjà utilisé. Veuillez en choisir un autre.")
        return code

    def clean(self):
        """
        Validation globale des dates.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(
                    "La date de début doit être antérieure à la date de fin."
                )
        return cleaned_data
    

class Annee_univForm(forms.ModelForm):
    class Meta:
        model = Annee_univ
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Exemple : 2024-2025',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'name': "Année universitaire",
            'start_date': "Date de Début",
            'end_date': "Date de Fin",
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if Annee_univ.objects.filter(code=code).exists():
            raise ValidationError("Ce code est déjà utilisé. Veuillez en choisir un autre.")
        return code

    def clean(self):
        """
        Validation globale des dates.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(
                    "La date de début doit être antérieure à la date de fin."
                )
        return cleaned_data



class VolumeHoraireForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )

    class Meta:
        model = Volume_horaire
        fields = ['heures']
        widgets = {
            'heures': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Volume horaire en heures',
                'oninput': 'updateCredits()',
            }),
        }
    
    credit = forms.IntegerField(
        required=False,
        label="Crédit",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'placeholder': 'Calculé automatiquement',
        }) 

    )

class GradeForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
  
    class Meta:
        model = Grade
        fields = ['code', 'label', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de grade'}),
            'description': CKEditorWidget(),  # Utilisation de CKEditorWidget
            }


