# forms.py
from django import forms
from .models import Sheet, Enseignements
from formset.collection import FormCollection
from formset.renderers.bootstrap import FormRenderer
from formset.views import FormCollectionView

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


class FinalFormCollection(FormCollection):
    default_renderer = FormRenderer(field_css_classes='mb-3')
    sheet = SheetForm()
    enseignement = EnseignementsForm()
