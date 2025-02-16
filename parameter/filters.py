from django_filters.filters import *
import django_filters
from django import forms
from parameter import models as pars_models
from django.db import models
from django_filters import CharFilter, ModelChoiceFilter



class ModuleFilterSet(django_filters.FilterSet):
    
    ufr = ModelChoiceFilter(
        queryset=pars_models.UniteDeRecherche.objects.all(),
        field_name="ufr",
        label="UFR.",
        empty_label="Rechercher par UFR."
    )
    departement = ModelChoiceFilter(
        queryset=pars_models.Departement.objects.all(),
        field_name="departement",
        label="Département.",
        empty_label="Rechercher par département."
    )
    ue = ModelChoiceFilter(
        queryset=pars_models.UE.objects.all(),
        field_name="ue",
        label="Unité.",
        empty_label="Rechercher par unité."
    )


    class Meta:
        model = pars_models.Module
        fields = {
            'label': ['exact', 'icontains'], 
            'ufr': ['exact'],  
            'departement': ['exact'],
            'ue': ['exact'],
        }
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs) 