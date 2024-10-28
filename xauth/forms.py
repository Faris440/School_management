from datetime import timedelta, date
from django import forms as fm

# from typing import Any
from django.forms import forms, fields, widgets
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
from django.utils.safestring import mark_safe
from django.conf import settings

from parameter import models as params_models
from xauth.models import User, Assign, AccountActivationSecret

MINIMUM_AGE = 0 * 365


class GroupForm( ModelForm):
  

    def __init__(self,  **kwargs):
        user = kwargs.pop("user", None)
        super().__init__( **kwargs)
        
        permissions = Permission.objects.filter(
            content_type__app_label__in=[
                "xauth",
                "parameter",
                "assign",
            ]
        )
        '''permissions = permissions.exclude(
            content_type__model__in=[
                "assign",
                "accountactivationsecret",
                "historicalassign",
            ]
        )'''
        
        
        if user   and  (not user.is_staff ):
            permissions=user.assign.group_assign.permissions.all(
         
        )
        self.fields["permissions"].queryset = permissions
       

       


    class Meta:
        model = Group
        fields = "__all__"
      


class CustomSetPasswordForm( SetPasswordForm):
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.is_active = True
        self.user.save()

        return self.user


class UserCreateForm( ModelForm):
    

    def __init__(self, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['birthplace'].required = True
        self.fields['email'].required = True
        self.fields['matricule'].required = True
        self.fields['address'].required = True
        self.fields['phone'].required = True
        
    

       
        for field in self.fields.values():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: red;'>*</span>")

        
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")

        if user_type == User.USER_TYPES.student:
            self.instance.is_student = True
        elif user_type == User.USER_TYPES.admin:
            self.instance.is_admin = True
        elif user_type == User.USER_TYPES.teacher:
            self.instance.is_teacher = True
     
        return cleaned_data

    class Meta:
        model = User
        fields = [
           # "photo",
            "user_type",
            "first_name",
            "last_name",
            "birthdate",
            "birthplace",
            "email",
            "matricule",
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
            "last_name": fm.TextInput(
                attrs={"placeholder": "Saisir votre prônom", "class":"form-control"},
            ),
            "phone": fm.TextInput(
                attrs={"placeholder": "Saisir votre numéro de téléphone", "class":"form-control"},
            ),
            "email": fm.EmailInput(
                attrs={"placeholder": "Saisir votre adresse e-mail", "class":"form-control"},
            ),
}
       
        labels = {
            "email": "Adresse email",
            "address": "Adresse",
            'matricule': "Matricule",
        }




class UserChangeForm( ModelForm):
   

    class Meta:
        model = User
        fields = [
            "user_type",
            "first_name",
            "last_name",
            "birthplace",
            "email",
            "matricule",
            "address",
            "phone",
        ]
       
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


class UserChangeProfilePhotoForm( ModelForm):

    class Meta:
        model = User
        fields = ("photo",)


class UserPublicActivationForm(forms.Form):
    identifier = fields.CharField(
        max_length=120,
        label="Identifiant",
        help_text="Vous pouvez saisir soit votre email ou votre matricule",
    )
    secret = fields.CharField(
        max_length=120,
        label="Code secret",
        help_text="Il s'agit du code que vous avez reçu par mail/sms",
    )


    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data["identifier"]
        secret = cleaned_data["secret"]

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    class Meta:
        model = Assign
        fields = ["group_assign", "nomination_date", "effective_date"]
       


class RoleForm(ModelForm):
   
    #
    def __init__(self, user: User = None, **kwargs):
        super().__init__( **kwargs)
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
