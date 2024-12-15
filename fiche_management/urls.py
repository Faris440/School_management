from django.urls import path
from fiche_management import views
# from .views import NotificationsListView



app_name = 'fiche_management'

urlpatterns = [
    path('management/download/<uuid:pk>/',view=views.DynamicNameView.as_view(), name='download-view'),
    path(
        "management/list/",
        view=views.SheetListView.as_view(),
        name="sheet-list",
        ),
    path(
        "management/create/",
        view=views.SheetPermananteCreateByAgentView.as_view(),
        name="sheet-create",
        ),
    path(
        "management/permanents/<str:type>/create/",
        view=views.SheetPermananteCreateByAgentView.as_view(),
        name="sheet-permanent-create",
        ),
    path(
        "management/vacataires/<str:type>/create/",
        view=views.SheetVacataireCreateByAgentView.as_view(),
        name="sheet-vacataire-create",
        ),
    path(
        "management/<uuid:pk>/detail/",
        view=views.SheetDetailView.as_view(),
        name="sheet-detail",
    ),
    path(
        "management/<uuid:pk>/update/",
        view=views.SheetUpdateView.as_view(),
        name="sheet-update",
    ),
    path(
        "management/<uuid:pk>/delete/",
        view=views.SheetDeleteView.as_view(),
        name="sheet-delete",
    ),

    path(
        "management/enseignement/<uuid:pk>/update/",
        view=views.EnseignementUpdateView.as_view(),
        name="enseignement-update",
    ),
    path(
        "management/enseignement/<uuid:pk>/delete/",
        view=views.EnseignementDeleteView.as_view(),
        name="enseignement-delete",
    ),

    path('management/sheet/<uuid:pk>/valider/',
         views.valider_fiche, 
         name='valider_fiche'),

    path('management/valider/enseignement/<uuid:pk>/',
        views.valider_enseignement, 
        name='valider_enseignement'),
    path('management/rejeter/enseignement/<uuid:pk>/',
        views.rejeter_enseignement, 
        name='rejeter_enseignement'),

    path('management/<uuid:pk>/rejeter/', 
         views.rejeter_fiche, 
         name='rejeter_fiche'),
    path(
        "management/enseignement/<uuid:pk>/update/",
        view=views.EnseignemtUpdateView.as_view(),
        name="enseignement-update",
    ),
    path('sheet/preview/', views.SheetPreviewView.as_view(),
      name='sheet_preview'),

    path('sheet/PermanentPreview/', views.SheetPermanantPreviewView.as_view(),
      name='perm_sheet_preview'),

    
    path('sheet/batch-validate-or-reject/', views.batch_validate_or_reject, name='batch_validate_or_reject'),

]
