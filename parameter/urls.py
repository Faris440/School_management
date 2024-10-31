from django.urls import path
from .views import *
from parameter import views


app_name = 'parameter'

urlpatterns = [

    path(
        "parameters/ufr/list/",
        view=views.UfrListView.as_view(),
        name="uniteDeRecherche-list",
    ),
    path(
        "parameters/ufr/create/",
        view=views.UfrCreateView.as_view(),
        name="uniteDeRecherche-create",
    ),
    path(
        "parameters/ufr/<uuid:pk>/detail/",
        view=views.UfrDetailView.as_view(),
        name="uniteDeRecherche-detail",
    ),
    path(
        "parameters/ufr/<uuid:pk>/update/",
        view=views.UfrUpdateView.as_view(),
        name="uniteDeRecherche-update",
    ),
    path(
        "parameters/ufr/<uuid:pk>/delete/",
        view=views.UfrDeleteView.as_view(),
        name="uniteDeRecherche-delete",
    ),


    ##Departements urls

    path(
        "parameters/departement/list/",
        view=views.DepartementListView.as_view(),
        name="departement-list",
    ),
    path(
        "parameters/departement/create/",
        view=views.DepartementCreateView.as_view(),
        name="departement-create",
    ),
    path(
        "parameters/departement/<uuid:pk>/detail/",
        view=views.DepartementDetailView.as_view(),
        name="departement-detail",
    ),
    path(
        "parameters/departement/<uuid:pk>/update/",
        view=views.DepartementUpdateView.as_view(),
        name="departement-update",
    ),
    path(
        "parameters/departement/<uuid:pk>/delete/",
        view=views.DepartementDeleteView.as_view(),
        name="departement-delete",
    ),


    ##filieres urls

    path(
        "parameters/filiere/list/",
        view=views.FiliereListView.as_view(),
        name="filiere-list",
    ),
    path(
        "parameters/filiere/create/",
        view=views.FiliereCreateView.as_view(),
        name="filiere-create",
    ),
    path(
        "parameters/filiere/<uuid:pk>/detail/",
        view=views.FiliereDetailView.as_view(),
        name="filiere-detail",
    ),
    path(
        "parameters/filiere/<uuid:pk>/update/",
        view=views.FiliereUpdateView.as_view(),
        name="filiere-update",
    ),
    path(
        "parameters/filiere/<uuid:pk>/delete/",
        view=views.FiliereDeleteView.as_view(),
        name="filiere-delete",
    ),
    
     ##niveau urls

     path(
         "parameters/niveau/list/",
         view=views.NiveauListView.as_view(),
         name="niveau-list",
     ),
     path(
         "parameters/niveau/create/",
         view=views.NiveauCreateView.as_view(),
         name="niveau-create",
     ),
    path(
        "parameters/niveau/<uuid:pk>/detail/",
         view=views.NiveauDetailView.as_view(),
         name="niveau-detail",
     ),
     path(
         "parameters/niveau/<uuid:pk>/update/",
         view=views.NiveauUpdateView.as_view(),
         name="niveau-update",
     ),
     path(
        "parameters/niveau/<uuid:pk>/delete/",
         view=views.NiveauDeleteView.as_view(),
         name="niveau-delete",
     ),
    
    
    ##semestre urls

    path(
        "parameters/semestre/list/",
        view=views.SemestreListView.as_view(),
        name="semestre-list",
    ),
    path(
        "parameters/semestre/create/",
        view=views.SemestreCreateView.as_view(),
        name="semestre-create",
    ),
    path(
        "parameters/semestre/<uuid:pk>/detail/",
        view=views.SemestreDetailView.as_view(),
        name="semestre-detail",
    ),
    path(
        "parameters/semestre/<uuid:pk>/update/",
        view=views.SemestreUpdateView.as_view(),
        name="semestre-update",
    ),
    path(
        "parameters/semestre/<uuid:pk>/delete/",
        view=views.SemestreDeleteView.as_view(),
        name="semestre-delete",
    ),
    
        ##UE urls

    path(
        "parameters/ue/list/",
        view=views.UeListView.as_view(),
        name="ue-list",
    ),
    path(
        "parameters/ue/create/",
        view=views.UeCreateView.as_view(),
        name="ue-create",
    ),
    path(
        "parameters/ue/<uuid:pk>/detail/",
        view=views.UeDetailView.as_view(),
        name="ue-detail",
    ),
    path(
        "parameters/ue/<uuid:pk>/update/",
        view=views.UeUpdateView.as_view(),
        name="ue-update",
    ),
    path(
        "parameters/ue/<uuid:pk>/delete/",
        view=views.UeDeleteView.as_view(),
        name="ue-delete",
    ),
    
    
    ##module urls

    path(
        "parameters/modules/list/",
        view=views.ModuleListView.as_view(),
        name="module-list",
    ),
    path(
        "parameters/modules/create/",
        view=views.ModuleCreateView.as_view(),
        name="module-create",
    ),
    path(
        "parameters/modules/<uuid:pk>/detail/",
        view=views.ModuleDetailView.as_view(),
        name="module-detail",
    ),
    path(
        "parameters/modules/<uuid:pk>/update/",
        view=views.ModuleUpdateView.as_view(),
        name="module-update",
    ),
    path(
        "parameters/modules/<uuid:pk>/delete/",
        view=views.ModuleDeleteView.as_view(),
        name="module-delete",
    ),
    


]
