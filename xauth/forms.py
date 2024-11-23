from datetime import timedelta, date
from django import forms as fm
from formset.widgets import (
    DualSortableSelector,DatePicker,UploadedFileInput,
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
from xauth.models import User, Assign, AccountActivationSecret, Nomination
from django.utils.timezone import now, timedelta 


from School_management.constants import *

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


class UserCreateForm(FormMixin, ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-6 h-100 input100",
            "photo": "mb-5 col-md-6",
        },
    )

    def __init__(self, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['birthplace'].required = True
        self.fields['email'].required = True
        self.fields['address'].required = True
        self.fields['phone'].required = True
        self.fields['ufr'].required = False        
        self.fields['departement'].required = False        
        self.fields['filiere'].required = False        
        self.fields['matricule'].required = False        
    

       
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
     
        return cleaned_data

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
            "email",
            "matricule",
            "grade",
            "date_nomination",
            "diplome",
            "ufr",
            "departement",
            "filiere",
            "structure_origine",
            "address",
            "phone",
        ]
        widgets = {
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
            "phone": fm.TextInput(
                attrs={"placeholder": "Saisir votre numéro de téléphone", "class":"form-control"},
            ),
            "email": fm.EmailInput(
                attrs={"placeholder": "Saisir votre adresse e-mail", "class":"form-control"},
            ),
            "birthdate" : DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            "date_nomination" : DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            
}
       
        labels = {
            "email": "Adresse email",
            "address": "Adresse",
            'matricule': "Matricule",
        }

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
            "user_type",
            "first_name",
            "last_name",
            "birthplace",
            "email",
            "matricule",
            "address",
            "phone",
        ]
        widgets = {
            "photo": UploadedFileInput(attrs={"max-size": 1024 * 1024 * 3}),
        }

       
        labels = {
            "email": "Adresse email",
            "matricule": "Nom d'utilisateur",
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