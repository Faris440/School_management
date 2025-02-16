from django.urls import path

from xauth import views

app_name = "auth"

urlpatterns = [
    # User
    path("users/create/", views.UserCreateView.as_view(), name="user-create"),


    path("users/list/", views.UserListView.as_view(), name="user-list"),
  
    path("users/staff/list/", views.StaffListView.as_view(), name="staff-list"),
    path(
        "users/<uuid:pk>/edit/",
        views.UserUpdateView.as_view(),
        name="user-update",
    ),
    path(
        "users/<uuid:pk>/edit/photo",
        views.UserProfilePhotoUpdateView.as_view(),
        name="user-update-photo",
    ),
    path(
        "users/<uuid:pk>/detail/",
        views.UserDetailView.as_view(),
        name="user-detail",
    ),
    path(
        "users/<uuid:pk>/delete/",
        views.UserDeleteView.as_view(),
        name="user-delete",
    ),
    path(
        "users/<uuid:pk>/password/",
        views.UserUpdatePasswordView.as_view(),
        name="user-update-password",
    ),
    path(
        "users/<uuid:pk>/make-admin/",
        views.UserAdminRightView.as_view(),
        name="user-make-admin",
    ),
    path(
        "users/<uuid:pk>/send-activation-key/",
        views.UserSendSecreteKey.as_view(),
        name="user-send-key",
    ),
    # Group
    path("groups/create/", views.GroupCreateView.as_view(), name="group-create"),
    path(
        "groups/<int:pk>/update/",
        views.GroupUpdateView.as_view(),
        name="group-update",
    ),
    path("groups/list/", views.GroupListView.as_view(), name="group-list"),
    path(
        "groups/<int:pk>/delete/",
        views.GroupDeleteView.as_view(),
        name="group-delete",
    ),
    path(
        "groups/<int:pk>/detail/",
        views.GroupDetailView.as_view(),
        name="group-detail",
    ),
    # Assign
    # path(
    #     "users/nomination/<uuid:pk>/create/",
    #     views.AssignCreateView.as_view(),
    #     name="nomination-create",
    # ),
    path(
        "users/nomination/<uuid:pk>/create/",
        views.RoleCreateView.as_view(),
        name="nomination-create",
    ),
    # Liste des nominations (Vue basée sur la classe)
    path(
        'nominations/list', views.NominationListView.as_view(), 
        name='nominations-list'),

    # Détail d'une nomination (Vue basée sur la classe)
    path(
        'nominations/<uuid:pk>/', views.NominationDetailView.as_view(),
        name='nominations-detail'),

    # Création d'une nouvelle nomination (Vue basée sur la classe)
    path(
        'nominations/new/', views.NominationCreateView.as_view(),
        name='nominations-create'),

    # Mise à jour d'une nomination (Vue basée sur la classe)
    path(
        'nominations/<uuid:pk>/edit/', views.NominationUpdateView.as_view(), 
        name='nominations-update'),

    # Suppression d'une nomination (Vue basée sur la classe)
    path(
        'nominations/<uuid:pk>/delete/', views.NominationDeleteView.as_view(), 
        name='nominations-delete'),

    path(
        'nominations/<uuid:pk>/deactivate/', views.AssignRemoveView.as_view(), 
        name='nominations-deactivate'),
    path(
        "users/assign/<uuid:pk>/remove/",
        views.AssignRemoveView.as_view(),
        name="assign-remove",
        ),
    # path('users/<uuid:pk>/assign-modules/', views.AssignModuleListView.as_view(), name='assign-modules'),
    path(
        "users/nomination/<uuid:pk>/create/",
        views.RoleCreateView.as_view(),
        name="nomination-create",
    ),
    # Liste des nominations (Vue basée sur la classe)
    path(
        'attribut_module/list', views.AssignModuleListView.as_view(), 
        name='attributmodule-list'),

    # Détail d'une nomination (Vue basée sur la classe)
    path(
        'attribut_module/<uuid:pk>/', views.AssignModuleDeleteView.as_view(),
        name='attributmodule-detail'),

    # Création d'une nouvelle nomination (Vue basée sur la classe)
    path(
        'attribut_module/new/', views.AssignModuleCreateView.as_view(),
        name='attributmodule-create'),

    # Mise à jour d'une nomination (Vue basée sur la classe)
    path(
        'attribut_module/<uuid:pk>/edit/', views.AssignModuleUpdateView.as_view(), 
        name='attributmodule-update'),

    # Suppression d'une nomination (Vue basée sur la classe)
    path(
        'attribut_module/<uuid:pk>/delete/', views.AssignModuleDeleteView.as_view(), 
        name='attributmodule-delete'),

    path(
        'attribut_user_module/<uuid:pk>/update/', views.UserModulesUpdateView.as_view(), 
        name='attributmodule-update'),

]
