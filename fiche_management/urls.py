from django.urls import path
from fiche_management import views


app_name = 'fiche_management'

urlpatterns = [

    path(
        "management/list/",
        view=views.SheetListView.as_view(),
        name="sheet-list",
        ),
     path(
        "management/create/",
        view=views.SheetCreateView.as_view(),
        name="sheet-create",
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

]
