from django import forms
from .models import MailContent, UniteDeRecherche, Departement, Filiere, UE, Module, Semestre,Niveau,Promotion
from django.forms.models import ModelChoiceField , ModelMultipleChoiceField
from formset.renderers.bootstrap import FormRenderer
from formset.widgets import (
    Selectize,
    SelectizeMultiple,
    DualSortableSelector,
    DualSelector,
    Selectize,
)
from formset.collection import FormMixin
from formset.richtext.widgets import RichTextarea
from django.utils.safestring import mark_safe
from School_management.constants import control_elements , TEXTAREA
from django.core.exceptions import ValidationError



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
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
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
        fields = ['code', 'departement', 'label', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la filière'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
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
    
    semestres = ModelMultipleChoiceField(
        queryset=Semestre.objects.all(),
        label="Semestres",
        widget=SelectizeMultiple(
            search_lookup="label__icontains",
        )
    )
    
    class Meta:
        model = Niveau
        fields = ['code', 'label', 'semestres','description']
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
        fields = ['code', 'label', 'description',]  # Ajout du champ 'semestre'
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du semestre'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            
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
            'filiere': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez la filiere",
            ),
            # 'departement': Selectize(
            #     attrs={'class': 'form-control', 'incomplete': True},
            #     search_lookup="label__icontains",
            #     placeholder="Sélectionnez un département",
            #     filter_by={"ufr": "ufr__id"},
            # ),
            # 'filiere': Selectize(
            #     attrs={'class': 'form-control', 'incomplete': True},
            #     search_lookup="label__icontains",
            #     placeholder="Sélectionnez une filière",
            #     filter_by={"departement": "departement__id"},  # Liaison au département sélectionné
            # ),
        }

class ModuleForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
    class Meta:
        model = Module
        fields = [
            'code', 'label', 'description', 'ufr', 'departement', 
            'filiere', 'niveau', 'semestre', 'ue', 'volume_horaire', 'credit'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du module'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'ufr': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez une UFR",
            ),
            'departement': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez un département",
                filter_by={"ufr": "ufr__id"},
            ),
            'filiere': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez une filière",
                filter_by={"departement": "departement__id"},  # Liaison au département sélectionné
            ),
            'ue': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez une unité d'enseignement",
                filter_by={"filiere": "filiere__id"},  # Liaison au département sélectionné
            ),

        }
       
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



