# forms.py
from django import forms
from .models import Sheet, Enseignements
from formset.collection import FormCollection
from formset.renderers.bootstrap import FormRenderer
from formset.views import FormCollectionView
from formset.widgets import DatePicker, Selectize
from django.utils.timezone import now, timedelta
from formset.collection import FormMixin
from xauth.models import User
from django.utils.safestring import mark_safe


class EnseignementsForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
    class Meta:
        model = Enseignements
        fields = [
            'code','filiere', 'niveau', 'semestre', 'module',
            'ct_volume_horaire_confie', 'td_volume_horaire_confie', 'tp_volume_horaire_confie',
            'ct_volume_horaire_efectue', 'td_volume_horaire_efectue', 'tp_volume_horaire_efectue'
        ]


class SheetForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
    
    class Meta:
        model = Enseignements
        fields = [
            'code','filiere', 'niveau', 'semestre', 'module',
            'ct_volume_horaire_confie', 'td_volume_horaire_confie', 'tp_volume_horaire_confie',
            'ct_volume_horaire_efectue', 'td_volume_horaire_efectue', 'tp_volume_horaire_efectue'
        ]


# Soumission d'une fiche d'un enseignant permanant par un admin
class SheetAgentPermanantForm(FormMixin, forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-4 input100s",
        },
    )
    etablissement_enseigne = forms.CharField(label= "Etablissement beneficier")
    volume_horaire_statuaire = forms.IntegerField(label= "Volume horaire statuaire")

    class Meta:
        model = Sheet
        fields = [
        'enseignant',
        'date_debut',
        'date_fin',
        'etablissement_enseigne',
        'volume_horaire_statuaire',
        'abattement',
        'motif_abattement',
        'v_h_obli_apres_abattement',
        ]
        widgets = {
            'date_fin' : DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
            'date_debut': DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
            'etablissement_enseigne' : forms.TextInput(attrs={'class': 'form-control',}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['etablissement_enseigne'].required = True
        self.fields['enseignant'].queryset = User.objects.filter(teacher_type = 'permanent')
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: red;'>*</span>"
                )
    
    
        
# Soumission d'une fiche d'un enseignant vacataire par un admin
class SheetAgentVacataireForm(FormMixin, forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-4 input100s",
        },
    )
    class Meta:
        model = Sheet
        fields = ['enseignant','etablissement_enseigne','date_debut','date_fin']
        widgets = {
            'date_fin' : DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
            'date_debut': DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
            'enseignant' : Selectize()
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['etablissement_enseigne'].required = True
        self.fields['etablissement_enseigne'].required = True
        self.fields['enseignant'].queryset = User.objects.filter(teacher_type = 'vacataire')
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: red;'>*</span>"
                )


class SheetPermanentForm(FormMixin, forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-4 input100s",
        },
    )
    class Meta:
        model = Sheet
        fields = [
         'date_debut',
         'date_fin',
         'etablissement_enseigne',
         'volume_horaire_statuaire',
         'abattement',
         'motif_abattement',
         'v_h_obli_apres_abattement',
         ]
        widgets = {
            'date_fin' : DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
            'date_debut': DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
        }

class SheetVacataireForm(FormMixin, forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-4 input100s",
        },
    )
    class Meta:
        model = Sheet
        fields = [
         'date_debut',
         'date_fin',
         'etablissement_enseigne',
         ]
        widgets = {
            'date_fin' : DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
            'date_debut': DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
        }

class SheetSelfForm(FormMixin, forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-4 input100s",
        },
    )
    class Meta:
        model = Sheet
        fields = ['date_debut', 'date_fin']


class LogCollection(FormCollection):
    min_siblings = 1
    add_label = "Ajouter un enseignement"
    log = EnseignementsForm()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

# form finale d'une fiche d'un enseignant permanant par un admin
class FinalAgentPermanentFormCollection(FormCollection):
    sheet = SheetAgentPermanantForm()
    enseignement = LogCollection()

    
# form final d'une fiche d'un enseignant vacataire par un admin
class FinalAgentVacataireFormCollection(FormCollection):
    sheet = SheetAgentVacataireForm()
    enseignement = LogCollection()


# form finale d'une fiche d'un enseignant permanant
class FinalPermanentFormCollection(FormCollection):
    default_renderer = FormRenderer(field_css_classes='mb-3')
    sheet = SheetPermanentForm()
    enseignement = LogCollection()


# form finale d'une fiche d'un enseignant vacataire
class FinalVacataireFormCollection(FormCollection):
    default_renderer = FormRenderer(field_css_classes='mb-3')
    sheet = SheetVacataireForm()
    enseignement = LogCollection()

class FinalSelfFormCollection(FormMixin ,FormCollection):
    default_renderer = FormRenderer(field_css_classes='mb-3')
    sheet = SheetSelfForm()
    enseignement = LogCollection()




class SheetFormu(FormMixin, forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-4 input100s",
        },
    )
    class Meta:
        model = Sheet
        fields = ['enseignant','etablissement_enseigne','date_debut','date_fin']
        widgets = {
            'date_fin' : DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
            'date_debut': DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
            'enseignant' : Selectize()
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['etablissement_enseigne'].required = True
        self.fields['etablissement_enseigne'].required = True
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: red;'>*</span>"
                )
