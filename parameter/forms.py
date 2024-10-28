from django import forms
from .models import UniteDeRecherche, Departement, Filiere, UE, Module, Semestre,Niveau
from django.forms.models import ModelChoiceField , ModelMultipleChoiceField
from formset.widgets import (
    Selectize,
    SelectizeMultiple,
    DualSortableSelector,
    DualSelector
)
from formset.collection import FormMixin

class UniteDeRechercheForm(forms.ModelForm):
    class Meta:
        model = UniteDeRecherche
        fields = ['code', 'label', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'Unité de Recherche'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['code', 'label', 'description', 'ufr']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du département'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'unite_de_recherche': forms.Select(attrs={'class': 'form-control'}),
        }


class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = ['code', 'label', 'description', 'departement']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la filière'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'departement': forms.Select(attrs={'class': 'form-control'}),
        }
        

class NiveauForm(forms.ModelForm):
    
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
    class Meta:
        model = Semestre
        fields = ['code', 'label', 'description',]  # Ajout du champ 'semestre'
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du semestre'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            
        }

class UEForm(forms.ModelForm):
    class Meta:
        model = UE
        fields = ['code', 'label', 'description', 'filiere']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'UE'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'filiere': forms.Select(attrs={'class': 'form-control'}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['code', 'label', 'description','ue']  # Ajout du champ 'ue'
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du module'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'ue': forms.Select(attrs={'class': 'form-control'}),
        }
        


