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
from django.forms import widgets


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
            'code', 'niveau', 'semestre', 'module','filiere',
            'ct_volume_horaire_confie', 'td_volume_horaire_confie', 'tp_volume_horaire_confie',
        ]

class VacataireEnseignementsForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
    class Meta:
        model = Enseignements
        fields = [
            'code', 'filiere', 'niveau', 'semestre', 'module',
            'ct_volume_horaire_confie', 'td_volume_horaire_confie', 'tp_volume_horaire_confie',
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
            'code', 'niveau', 'semestre', 'module',
            'ct_volume_horaire_confie', 'td_volume_horaire_confie', 'tp_volume_horaire_confie',
        ]


# Soumission d'une fiche d'un enseignant permanant par un admin
class SheetAgentPermanantForm(FormMixin, forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-4 input100s",
        },
    )
    etablissement_enseigne = forms.CharField(label="Etablissement bénéficiaire")
    gender = forms.fields.ChoiceField(
            label="Permanent",
            choices=[('O', "Oui"), ('N', "Non")],
            widget=widgets.RadioSelect,
                )
    
    class Meta:
        model = Sheet
        fields = [
            'enseignant',
            'promotion',
            'date_debut',
            'date_fin',
            'etablissement_enseigne',
            'volume_horaire_statuaire',
            'abattement',
            'motif_abattement',
            'promotion',
            
        ]

        widgets = {
            'date_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'df-show': ".gender=='O'"
            }),
            'date_debut': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'df-show': ".gender=='O'"
            }),
            'etablissement_enseigne': forms.TextInput(attrs={'class': 'form-control'}),
            'volume_horaire_statuaire' : forms.NumberInput(attrs={'df-show': ".gender=='O'"}),
            'abattement' : forms.NumberInput(attrs={'df-show': ".gender=='O'"}),
            'motif_abattement' : forms.TextInput(attrs={'df-show': ".gender=='O'"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Définir une valeur par défaut pour le champ `etablissement_enseigne`
        default_value = "Université Virtuelle du Burkina Faso (UV-BF)"  # Remplacez par la valeur souhaitée
        self.fields['etablissement_enseigne'].initial = default_value

        # Désactiver le champ pour empêcher sa modification
        self.fields['etablissement_enseigne'].disabled = True

        # Configurations spécifiques pour les champs obligatoires ou non
        self.fields['etablissement_enseigne'].required = False
        self.fields['volume_horaire_statuaire'].required = False
        self.fields['abattement'].required = False
        self.fields['motif_abattement'].required = False
        self.fields['date_debut'].required = False
        self.fields['date_fin'].required = False


        # Filtrer les enseignants de type "permanent"
        self.fields['enseignant'].queryset = User.objects.filter(teacher_type='permanent')

        # Ajouter une indication visuelle pour les champs requis
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
        fields = ['enseignant', 'etablissement_enseigne', 'promotion']
        widgets = {
            'enseignant': Selectize()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir une valeur par défaut pour le champ `etablissement_enseigne`
        default_value = "Université Virtuelle du Burkina Faso (UV-BF)"  # Remplacez par la valeur souhaitée
        self.fields['etablissement_enseigne'].initial = default_value
        
        # Désactiver le champ pour empêcher la modification
        self.fields['etablissement_enseigne'].disabled = True
        
        # Rendre ce champ obligatoire (même si désactivé)
        self.fields['etablissement_enseigne'].required = True
        
        # Filtrer les enseignants de type "vacataire"
        self.fields['enseignant'].queryset = User.objects.filter(teacher_type='vacataire')
        
        # Ajouter une indication visuelle pour les champs requis
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

    gender = forms.fields.ChoiceField(
            label="Permanent",
            choices=[('O', "Oui"), ('N', "Non")],
            widget=widgets.RadioSelect,
                )

    class Meta:
        model = Sheet
        fields = [
            'date_debut',
            'date_fin',
            'promotion',
            'etablissement_enseigne',
            'volume_horaire_statuaire',
            'abattement',
            'motif_abattement',
        ]
        widgets = {
            'date_fin': DatePicker(attrs={
                'max': (now()).isoformat(),
            'df-show': ".gender=='O'"
            }),
            'date_debut': DatePicker(attrs={
                'max': (now()).isoformat(),
            'df-show': ".gender=='O'"
            }),
            'etablissement_enseigne': forms.TextInput(attrs={'class': 'form-control'}),
            'volume_horaire_statuaire' : forms.NumberInput(attrs={'df-show': ".gender=='O'"}),
            'abattement' : forms.NumberInput(attrs={'df-show': ".gender=='O'"}),
            'motif_abattement' : forms.TextInput(attrs={'df-show': ".gender=='O'"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Définir une valeur par défaut pour le champ `etablissement_enseigne`
        default_value = "Université Virtuelle du Burkina Faso (UV-BF)"  # Remplacez par la valeur souhaitée
        self.fields['etablissement_enseigne'].initial = default_value

        # Désactiver le champ pour empêcher sa modification
        self.fields['etablissement_enseigne'].disabled = True

        self.fields['etablissement_enseigne'].required = False
        self.fields['volume_horaire_statuaire'].required = False
        self.fields['abattement'].required = False
        self.fields['motif_abattement'].required = False
        self.fields['date_debut'].required = False
        self.fields['date_fin'].required = False

        # Ajouter une indication visuelle pour les champs requis
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: red;'>*</span>"
                )




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
            'promotion',
            'etablissement_enseigne',
        ]
        widgets = {
            'etablissement_enseigne': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Définir une valeur par défaut pour le champ `etablissement_enseigne`
        default_value = "Université Virtuelle du Burkina Faso (UV-BF)"  # Remplacez par la valeur souhaitée
        self.fields['etablissement_enseigne'].initial = default_value

        # Désactiver le champ pour empêcher sa modification
        self.fields['etablissement_enseigne'].disabled = True

        # Ajouter une indication visuelle pour les champs requis
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: red;'>*</span>"
                )



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


class LogVacataireCollection(FormCollection):
    min_siblings = 1
    add_label = "Ajouter un enseignement"
    log = VacataireEnseignementsForm()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# form finale d'une fiche d'un enseignant permanant par un admin
class FinalAgentPermanentFormCollection(FormCollection):
    sheet = SheetAgentPermanantForm()
    enseignement = LogCollection()

    
# form final d'une fiche d'un enseignant vacataire par un admin
class FinalAgentVacataireFormCollection(FormCollection):
    sheet = SheetAgentVacataireForm()
    enseignement = LogVacataireCollection()


# form finale d'une fiche d'un enseignant permanant
class FinalPermanentFormCollection(FormCollection):
    default_renderer = FormRenderer(field_css_classes='mb-3')
    sheet = SheetPermanentForm()
    enseignement = LogCollection()


# form finale d'une fiche d'un enseignant vacataire
class FinalVacataireFormCollection(FormCollection):
    default_renderer = FormRenderer(field_css_classes='mb-3')
    sheet = SheetVacataireForm()
    enseignement = LogVacataireCollection()

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
