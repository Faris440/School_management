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
        ('teacher', 'Enseignant'),
        ('agent_administratif', 'Personnel administratif'),
    )
    MATRIAL_STATUS = Choices(
        ('bachelor', 'Célibataire'),
        ('married', 'Mariée'),
        ('divorced', 'Divorcée'),
        ('widower', 'Veuve'),
    )
    TEACHER_TYPE_CHOICES = Choices(
        ('vacataire', 'Vacataire'),
        ('permanent', 'Permanent'),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default=USER_TYPES.teacher,
        verbose_name="Type d'utilisateur"
    )
    first_name = models.CharField(_("first name"), max_length=MEDIUM_LENGTH)
    last_name = models.CharField(_("last name"), max_length=MEDIUM_LENGTH)
    diplome = models.CharField(_("diplome"),null=True, max_length=MEDIUM_LENGTH)
    structure_origine = models.CharField(_("Struture d'origine"), max_length=MEDIUM_LENGTH)
    date_nomination = models.DateField(_("Date de nomination"), null=True, max_length=MEDIUM_LENGTH)
    birthdate = models.DateField("Date de naissance")
    last_name = models.CharField(_("last name"), max_length=MEDIUM_LENGTH)
    email = models.EmailField(_("email address"), unique=True)
    birthdate = models.DateField("Date de naissance")
    birthplace = models.CharField("Lieu de naissance", max_length=MIN_LENGTH)
    matricule = models.CharField(max_length=MIN_LENGTH, null=True, unique=True)
    address = models.CharField("Adresse", max_length=MIN_LENGTH, null=True, blank=True)
    photo = models.ImageField(
        "Photo d'identité",
        null=True,
        blank=True,
        help_text="Une image dont la taille n'excède pas 3 Mo",
        upload_to="profil/",
    )
    phone = PhoneNumberField("Numéro de téléphone", unique=True)
    is_admin = models.BooleanField(verbose_name="Est un(e) administrateur(e)", default=False)
    is_teacher = models.BooleanField(verbose_name="Est un(e) enseignant(e)", default=False)
    is_president = models.BooleanField(verbose_name="Est un(e) vice président(e)", default=False)
    is_finance = models.BooleanField(verbose_name="Est une chaine financière", default=False)

    marital_status = models.CharField(
        max_length=20,
        verbose_name="Situation matrimoniale",
        choices=MATRIAL_STATUS,
        default=MATRIAL_STATUS.bachelor,
    )
    nationality = models.CharField(
        verbose_name="Nationalité",
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
    teacher_type = models.CharField(
        max_length=10,
        choices=TEACHER_TYPE_CHOICES,
        verbose_name="Type d'enseignant",
        null=True,
        blank=True,
        help_text="Indiquez si l'enseignant est vacataire ou permanent",
    )
    grade = models.CharField("Grade", max_length=MEDIUM_LENGTH, null=True, blank=True)
    diplome = models.CharField("Diplôme", max_length=MEDIUM_LENGTH, null=True, blank=True)
    ufr = models.ForeignKey('parameter.UniteDeRecherche', on_delete=models.CASCADE,null=True, related_name="user_urf")
    departement = models.ForeignKey('parameter.Departement', on_delete=models.CASCADE,null=True, related_name="user_department")
    filiere = models.ForeignKey('parameter.Filiere', on_delete=models.CASCADE,null=True, related_name="user_filiere")

    def save(self, *args, **kwargs):

        if self.user_type == self.USER_TYPES.agent_administratif:
            self.is_agent_administratif = True
            self.teacher_type = None
        elif self.user_type == self.USER_TYPES.teacher:
            self.is_teacher = True
            if not self.teacher_type:
                self.teacher_type = self.TEACHER_TYPE_CHOICES.vacataire  # par défaut
        else:
            self.teacher_type = None
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
            ("access_fiche_management", "Can access to fiche_management module"),
            ("access_xauth", "Can access to xauth module"),
            ("access_account", "Can access to account module"),
            ("can_submit_programmatic_sheet", "Peut soumettre une fiche programmatique"),
            ("can_update_programmatic_sheet", "Peut modifier une fiche programmatique"),
            ("can_delete_programmatic_sheet", "Peut supprimer une fiche programmatique"),
            ("can_download_programmatic_sheet", "peut telecharger une fiche programmatique"),
            ("can_export_programmatic_sheet", "Peut exporter une fiche programmatique"),
            ("can_validate_programmatic_sheet", "peut valider une fiche programmatique"),
            ("vice_president", "Est un vice président"),
            ("responsable_ufr", "Est responsable d'une ufr"),
            ("responsable_programme", "Est responsable d'un programme"),
            ("responsable_filiere", "Est responsable d'une filière"),
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

# class VolumeHoraireStatuaire(BaseModel):
#     class Meta:
#         ordering = ["label"]
#         verbose_name = "Volume horaire statutaire"
#         verbose_name_plural = "Volumes horaires statutaire"
#         permissions = [("list_volumeHoraireStatuaire", f"Peut lister {verbose_name}")]

#     def __str__(self):
#         return self.label


class Nomination(CommonAbstractModel):
    # Champ ForeignKey pour l'utilisateur (non nullable)
    user = models.ForeignKey(
        User,  # Si vous utilisez le modèle utilisateur par défaut de Django
        on_delete=models.CASCADE,
        related_name="nominations",
        null=False
    )

    # Champ de type choix pour la nomination
    NOMINATION_TYPE_CHOICES = [
        ('filiere', 'Filière'),
        ('ufr', 'UFR'),
        ('vise-president', 'Vice-président'),
    ]
    nomination_type = models.CharField(
        max_length=20,
        choices=NOMINATION_TYPE_CHOICES,
        null=False
    )

    # Champs ForeignKey pour les différentes entités (ufr, departement, filiere) avec possibilité d'être null
    ufr = models.ForeignKey(
        'parameter.UniteDeRecherche',  # Remplacez par le modèle réel pour UFR
        on_delete=models.SET_NULL,
        related_name="nominations_ufr",
        null=True,
        blank=True
    )
    
    departement = models.ForeignKey(
        'parameter.Departement',  # Remplacez par le modèle réel pour Département
        on_delete=models.SET_NULL,
        related_name="nominations_departement",
        null=True,
        blank=True
    )

    filiere = models.ForeignKey(
        'parameter.Filiere',        # Remplacez par le modèle réel pour Filière
        on_delete=models.SET_NULL,
        related_name="nominations_filiere",
        null=True,
        blank=True
    )

    # Champ date_debut qui est obligatoire
    date_debut = models.DateField(null=False)
    date_fin = models.DateField(null=True)
    is_desactivate = models.BooleanField("Est inactif", default=False)

    def __str__(self):
        return f"Nomination de {self.user} pour {self.nomination_type} - {self.date_debut}"

    class Meta:
        verbose_name = "Nomination"
        verbose_name_plural = "Nominations"
        ordering = ['date_debut']
