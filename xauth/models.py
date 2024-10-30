from collections import defaultdict
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from model_utils.choices import Choices
from datetime import date, datetime
from School_management.cmodels import CONSTRAINT, CommonAbstractModel
from School_management.constants import MEDIUM_LENGTH, MIN_LENGTH
from parameter import models as parameter_models
from phonenumber_field.modelfields import PhoneNumberField




# Create your models here.


class User(AbstractUser, CommonAbstractModel):
    USERNAME_FIELD = "matricule"
    GENDER_CHOICES = [
        ('F', 'Femme'),
        ('H', 'Homme'),
    ]
    USER_TYPES = Choices(
        ('admin', 'ADMINISTRATEUR'),
        ('student', 'Etudiant'),
        ('teacher', 'Enseignant'),
        # ('teacher_manager', 'Responsable de filière'),
         # ('vice_president', 'Vice Président'),
       
    )
    MATRIAL_STATUS = Choices(
        ('bachelor', 'Célibataire'),
        ('married', 'Mariée'),
        ('divorced', 'Divorcée'),
        ('widower', 'Veuve'),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default=USER_TYPES.student,
        verbose_name="Type d'utilisateur"
    )

    first_name = models.CharField(_("first name"), max_length=MEDIUM_LENGTH)
    last_name = models.CharField(_("last name"), max_length=MEDIUM_LENGTH)
    email = models.EmailField(_("email address"), unique=True)
    birthdate = models.DateField("Date de naissance")
    birthplace = models.CharField("Lieu de naissance", max_length=MIN_LENGTH)
    matricule = models.CharField(max_length=MIN_LENGTH, unique=True)
    address = models.CharField("Adresse", max_length=MIN_LENGTH, null=True, blank=True)
    matricule = models.CharField(max_length=MIN_LENGTH, unique=True)
    photo = models.ImageField(
        "Photo d'identité",
        null=True,
        blank=True,
        help_text="Une image dont la taille n'excède pas 3 Mo",
    )
    phone = PhoneNumberField("Numéro de téléphone", unique=True)
    is_student = models.BooleanField(verbose_name="Est un(e) étudiant(e)", default=False)
    is_admin = models.BooleanField(verbose_name="Est un(e) administrateur(e)", default=False)
    is_teacher = models.BooleanField(verbose_name="Est un(e) enseignant(e)", default=False)
    marital_status = models.CharField(
        max_length=20,
        verbose_name="Situation matrimonial",
        choices=MATRIAL_STATUS,
        default=MATRIAL_STATUS.bachelor,
    )
   
    nationality = models.CharField(verbose_name="Nationalité", 
                                   max_length=MIN_LENGTH, 
                                   null=True, 
                                   blank=True
                                   )
  

    
    gender = models.CharField(
        "Genre",
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )
    
    

    def save(self, *args, **kwargs):
        if self.user_type == self.USER_TYPES.student:
            self.is_student = True
        elif self.user_type == self.USER_TYPES.admin:
            self.is_admin = True
        elif self.user_type == self.USER_TYPES.teacher:
            self.is_teacher = True
        super().save(*args, **kwargs)
        
    
    def get_role(self):
        if self.is_staff:
            return "admin"
        elif hasattr(self, "assign"):
            return self.assign.group_assign.name
        else:
            return "-"

   


    def __str__(self):
            return f"{self.first_name} {self.last_name}"


    

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
        permissions = [
            ("list_user", "Can list user"),
            ("can_assign", "Peut attribuer un rôle"),
            ("deactivate_user", "Can deactivate user"),
            ("change_right_user", "Can change user right"),
            ("access_parameter", "Can access to parameter module"),
            ("access_account", "Can access to account module"),
            ("can_submit_programmatic_sheet","Peut soumettre une fiche programmatique"),
            ("can_download_programmatic_sheet","peut telecharger une fiche programmatique"),
            ("can_edit_progrmmatic_sheet","peut modifier une fiche programmatique"),
            ("can_validate_programmatic_sheet","peut valider une fiche programmatique")

        ]


class AccountActivationSecret(CommonAbstractModel):
    user = models.OneToOneField(User, on_delete=CONSTRAINT)
    secret = models.CharField(max_length=MIN_LENGTH)


class Assign(CommonAbstractModel):
    assigner = models.ForeignKey(
        User, on_delete=CONSTRAINT, related_name="assigner", null=True, blank=True
    )
    unassigner = models.ForeignKey(
        User, on_delete=CONSTRAINT, related_name="unassigner", null=True, blank=True
    )
    
    user = models.OneToOneField(
        User, on_delete=CONSTRAINT, related_name="assign", null=True, blank=True
    )

    nomination_date = models.DateField(null=True)
    effective_date = models.DateField(null=True)
    end_date = models.DateField(null=True, blank=True)
    group_assign = models.ForeignKey(
        "auth.Group", on_delete=CONSTRAINT, null=True, blank=True
    )
