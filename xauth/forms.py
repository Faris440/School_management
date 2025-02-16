from datetime import timedelta, date
from django import forms as fm
from formset.widgets import (
    DualSortableSelector,DatePicker,UploadedFileInput,Selectize,SelectizeMultiple

    )
# from typing import Any
from django.forms import forms, fields, widgets, DateInput
from django.forms.models import ModelForm, ModelChoiceField
from django.db.models import Q
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
    
    
)
from formset.utils import FormsetErrorList 
from formset.collection import FormMixin 
from django.utils.safestring import mark_safe 
from django.conf import settings 
from formset.renderers.bootstrap import FormRenderer 
from parameter import models as params_models
from xauth.models import AttributModule, User, Assign, AccountActivationSecret, Nomination
from django.utils.timezone import now, timedelta 
from formset.widgets import PhoneNumberInput

from School_management.constants import *
from django import forms
from formset.collection import FormCollection
from formset.renderers.bootstrap import FormRenderer
from formset.views import FormCollectionView
from formset.widgets import DatePicker, Selectize
from django.utils.timezone import now, timedelta
from formset.collection import FormMixin
from xauth.models import User
from django.utils.safestring import mark_safe
from django.forms import widgets

default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-12 h-100 input100",
        },
    )
MINIMUM_AGE = 0 * 365

class GroupForm(FormMixin, ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-12 h-100 input100",
            "permissions": "mb-2  fs-1 col-md-12 h-100 input100"
        },
    )
    class Meta:
        model = Group
        fields = "__all__"
        widgets = {
            "permissions": DualSortableSelector(
                search_lookup=["name__icontains"],
                group_field_name="content_type",
            )
        }

    def __init__(self, error_class=FormsetErrorList, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(error_class, **kwargs)
        
        permissions = Permission.objects.filter(
            content_type__app_label__in=[
                "xauth",
                "auth",
                "parameter",
                "assign",
                "fiche_management",
            ]
        )
        
        if user and (not user.is_staff and not user.is_superviseur):
            permissions=user.assign.group_assign.permissions.all()
        self.fields["permissions"].queryset = permissions
    


class CustomSetPasswordForm(SetPasswordForm):
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.is_active = True
        self.user.save()

        return self.user


class UserCreateForm(ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 h-100 input100",
            "photo": "mb-5 col-md-6",
        },
    )
    
    teacher_type = forms.fields.ChoiceField(
            label="Statut de l'enseignant",
            choices=[('permanent', "Permanent"), ('vacataire', "Vacataire")],
            widget=widgets.RadioSelect,
                )

    class Meta:
        model = User
        fields = [
            "photo",
            "user_type",
            "teacher_type",
            "first_name",
            "last_name",
            "birthdate",
            "birthplace",
            "nationality",
            "gender",
            "marital_status",
            "email",
            "matricule",
            "grade",
            "date_nomination",
            "etablissement_enseigne",
            "course_start_date",
            "course_end_date",
            "volume_horaire_statuaire",
            "abattement",
            "motif_abattement",
            "diplome",
            "structure_origine",
            "address",
            "phone",
        ]
        widgets = {

            'grade': Selectize(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Sélectionnez un grade",
            ),
    
            # 'filiere': Selectize(
            #     attrs={'class': 'form-control', 'incomplete': True},
            #     search_lookup="label__icontains",
            #     placeholder="Sélectionnez une filière",
            # ),
            # 'module': SelectizeMultiple(
            #     attrs={'class': 'form-control', 'incomplete': True},
            #     search_lookup="label__icontains",
            #     placeholder="Sélectionnez un module",
            #     filter_by={"filiere": "filiere__id"},  # Correction ici
            # ),

            # 'niveau': Selectize(
            #     attrs={'class': 'form-control', 'incomplete': True},
            #     search_lookup="label__icontains",
            #     placeholder="Sélectionnez le niveau",
            # ),
            # 'semestre': Selectize(
            #     attrs={'class': 'form-control', 'incomplete': True},
            #     search_lookup="label__icontains",
            #     placeholder="Sélectionnez le semestre",
            #     filter_by={"niveau": "niveau__id"}, 
            # ),
            # 'ue': Selectize(
            #     attrs={'class': 'form-control', 'incomplete': True},
            #     search_lookup="label__icontains",
            #     placeholder="Sélectionnez une filière",
            #     filter_by={"semestre": "semestre__id"}, 
            # ),


            "username": fm.TextInput(
                attrs={"placeholder": "Saisir votre nom d'utilisateur", "class":"form-control"},
            ),
            "first_name": fm.TextInput(
                attrs={"placeholder": "Saisir votre nom", "class":"form-control"},
            ),
            "photo": UploadedFileInput(attrs={"max-size": 1024 * 1024 * 3}),

            "last_name": fm.TextInput(
                attrs={"placeholder": "Saisir votre prénom", "class":"form-control"},
            ),
            "phone": PhoneNumberInput(
                attrs={
                    "mobile-only": True,
            }),
            "email": fm.EmailInput(
                attrs={"placeholder": "Saisir votre adresse e-mail", "class":"form-control"},
            ),
            "birthdate" : DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'etablissement_enseigne': forms.TextInput(attrs={'class': 'form-control'}),
            'volume_horaire_statuaire' : forms.NumberInput(attrs={'df-show': ".teacher_type=='permanent'"}),
            'abattement' : forms.NumberInput(attrs={'df-show': ".teacher_type=='permanent'"}),
            'motif_abattement' : forms.TextInput(attrs={'df-show': ".teacher_type=='permanent'"}),
            "matricule": forms.TextInput(attrs={'df-show': " .teacher_type=='permanent'", "class": "form-control"}),
            "date_nomination": forms.DateInput(attrs={'df-show': " .teacher_type=='permanent'", "class": "form-control", "type": "date"}),
            "course_start_date": forms.DateInput(attrs={'df-show': " .teacher_type=='permanent'", "class": "form-control", "type": "date"}),
            "course_end_date": forms.DateInput(attrs={'df-show': " .teacher_type=='permanent'", "class": "form-control", "type": "date"}),
        
        }
       
        labels = {
            "email": "Adresse email",
            "address": "Adresse",
            'matricule': "Matricule",
            "grade": "Grade",
            "date_nomination": "Date de nomination",
            "course_start_date": "Date de début du cours",
            "course_end_date": "Date de fin du cours",
            # "module" : "Modules confiées",

        }
    
    def __init__(self, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Définir une valeur par défaut pour le champ `etablissement_enseigne`
        default_value = "Université Virtuelle du Burkina Faso (UV-BF)"  # Remplacez par la valeur souhaitée
        self.fields['etablissement_enseigne'].initial = default_value

        # Désactiver le champ pour empêcher sa modification
        self.fields['etablissement_enseigne'].disabled = True

        # Ajout de l'attribut `max` pour empêcher les dates futures
        today = date.today().isoformat()  # Format 'YYYY-MM-DD'
        if "birthdate" in self.fields:
            self.fields["birthdate"].widget.attrs["max"] = today
        if "date_nomination" in self.fields:
            self.fields["date_nomination"].widget.attrs["max"] = today

        self.fields['user_type'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['birthplace'].required = False
        self.fields['birthdate'].required = False
        self.fields['email'].required = False
        self.fields['address'].required = False
        self.fields['phone'].required = True 
        # self.fields['filiere'].required = False        
        self.fields['matricule'].required = False        
        self.fields['grade'].required = False        
        self.fields['diplome'].required = False        
        # self.fields['module'].required = False        
        self.fields['date_nomination'].required = False        
        self.fields['matricule'].required = False        
        self.fields['date_nomination'].required = False        
        self.fields['course_start_date'].required = False        
        self.fields['course_end_date'].required = False        
        self.fields['structure_origine'].required = False        
        self.fields['volume_horaire_statuaire'].required = False        
        self.fields['abattement'].required = False        
        self.fields['motif_abattement'].required = False        
    

       
        for field in self.fields.values():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: red;'>*</span>")

        
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")

        if user_type == User.USER_TYPES.teacher:
            self.instance.is_teacher = True
        elif user_type == User.USER_TYPES.agent_administratif:
            self.instance.is_agent_administratif = True
        """
        Validation personnalisée des dates : La date de début ne doit pas être supérieure à la date de fin.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get("course_start_date")
        end_date = cleaned_data.get("course_end_date")

        if start_date and end_date and start_date > end_date:
            self.add_error("course_start_date", "La date de début ne peut pas être supérieure à la date de fin.")
            self.add_error("course_end_date", "La date de fin ne peut pas être inférieure à la date de début.")
     
        return cleaned_data




class UserChangeForm( ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-12 h-100 input100",
            "photo": "mb-5 col-md-6",
        },
    )

    class Meta:
        model = User
        fields = [
            "photo",
            "first_name",
            "last_name",
            "birthplace",
            "email",
            "address",
            "phone",
        ]
        widgets = {
            "photo": UploadedFileInput(attrs={"max-size": 1024 * 1024 * 3}),
        }

       
        labels = {
            "email": "Adresse email",
            }

    def __init__(self, **kwargs,):
        super().__init__(**kwargs)
        # self.fields['clinics'].required = False





class UserModulesForm( ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-12 h-100 input100",
            "photo": "mb-5 col-md-6",
        },
    )

    class Meta:
        model = User
        fields = [
            "module",
        ]
        widgets = {
            "module": DualSortableSelector(
                search_lookup=["name__icontains"],
                group_field_name="filiere",
            ),
        }

    def __init__(self, **kwargs,):
        super().__init__(**kwargs)
        # self.fields['clinics'].required = False



class UserConfirmDeleteForm(forms.Form):
    matricule = fields.CharField(max_length=120)

    def __init__(self, user=None, **kwargs):
        super().__init__( **kwargs)
        self.user = user

    def clean_matricule(self):
        matricule = self.cleaned_data.get("matricule")
        if matricule != self.user.matricule:
            raise forms.ValidationError("Le matricule ne correspond pas!")
        return matricule


class UserChangeProfilePhotoForm(FormMixin, ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-12 h-100 input100",
        },
    )
    class Meta:
        model = User
        fields = ["photo"]
        widgets = {
            "photo": UploadedFileInput(attrs={"max-size": 1024 * 1024 * 3}),
        }



class UserPublicActivationForm(FormMixin, forms.Form):
    identifier = fields.CharField(
        max_length=MIN_LENGTH,
        label="Identifiant",
        help_text="Vous pouvez saisir soit votre email ou votre matricule",
    )
    secret = fields.CharField(
        max_length=MIN_LENGTH,
        label="Code secret",
        help_text="Il s'agit du code que vous avez reçu par mail/sms",
    )

    default_renderer = default_renderer

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get("identifier")
        secret = cleaned_data.get("secret")

        user = User.objects.filter(Q(matricule=identifier) | Q(email=identifier))

        if not user.exists():
            raise forms.ValidationError(
                "Les informations fournies ne correspondent pas à un compte.",
                code="mismatch_account",
            )

        user = user.first()
        if user.is_active:
            raise forms.ValidationError(
                "Les informations fournies ne correspondent pas à un compte.",
                code="mismatch_account",
            )

        exist = AccountActivationSecret.available_objects.filter(
            user=user, secret=secret
        ).exists()
        if not exist:
            raise forms.ValidationError(
                "Les informations fournies ne correspondent pas à un compte.",
                code="mismatch_account",
            )
        cleaned_data["user"] = user
        return cleaned_data



class AssignForm( ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 h-100 input100",
        },
    )
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    class Meta:
        model = Assign
        fields = ["group_assign", "nomination_date", "effective_date"]
       


class RoleForm(ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 h-100 input100",
        },
    )
    #
    def __init__(self, user: User = None, **kwargs):
        super().__init__( **kwargs)
        self.fields['group_assign'].required = True
        if "instance" in kwargs and kwargs["instance"] is not None:
            # self.fields["structure"].widget.attrs["readonly"] = True
            pass

    class Meta:
        model = Assign
        fields = [
            "group_assign",
        ]
      
        labels = {
            "group_assign": "Rôle",
        }



class NominationForm(ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 input100s",
        },
    )
    class Meta:
        model = Nomination
        fields = ['user', 'nomination_type', 'ufr', 'departement', 'filiere', 'date_debut']
        widgets = {
            'date_debut': DatePicker(attrs={
                        'max': (now()).isoformat(),
                    }),
        }



class AttributModuleForm(ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={"*": "mb-2 col-md-6 input100s"},
    )

    # user = forms.ModelChoiceField(
    #     queryset=User.objects.filter(user_type="teacher"),
    #     widget=Selectize(attrs={'class': 'form-control','incomplete': True},
    #             search_lookup="label__icontains",
    #             placeholder="Sélectionnez une filière" ),
    #     required=True  # Empêche l'utilisateur de modifier ce champ
    # )

    class Meta:
        model = AttributModule
        fields = ['user', 'module']
        widgets = {
            'user' : Selectize(
                choices=User.objects.filter(user_type="teacher"),
            ),
            'module': SelectizeMultiple(
                attrs={'class': 'form-control', 'incomplete': True},
                search_lookup="label__icontains",
                placeholder="Module(s) à attribuer",
            ),
        }

    def __init__(self, *args, **kwargs):
        # self.teacher = kwargs.pop('teacher', None)  # Récupère l'enseignant depuis la vue
        super().__init__(*args, **kwargs)

    #    if self.teacher:
    #        self.fields['enseignant'].initial = self.teacher
