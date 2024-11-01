# forms.py
from django import forms
from .models import Sheet, Enseignements
from formset.collection import FormCollection
from formset.renderers.bootstrap import FormRenderer
from formset.views import FormCollectionView
from formset.widgets import DatePicker
from django.utils.timezone import now, timedelta


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

# Inclure le formset directement dans le formulaire principal
class SheetForm(forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-4 input100s",
        },
    )
    class Meta:
        model = Sheet
        fields = ['enseignant', 'date_debut', 'date_fin']
        widgets = {
            'date_fin' : DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
            'date_debut': DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
        }
        

class SheetSelfForm(forms.ModelForm):
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

class FinalFormCollection(FormCollection):
    default_renderer = FormRenderer(field_css_classes='mb-3')
    sheet = SheetForm()
    enseignement = LogCollection()


class FinalSelfFormCollection(FormCollection):
    default_renderer = FormRenderer(field_css_classes='mb-3')
    sheet = SheetSelfForm()
    enseignement = LogCollection()