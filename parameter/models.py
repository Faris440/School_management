from django.db import models
from School_management.cmodels import CONSTRAINT, CommonAbstractModel
import uuid
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField




# Définitions des longueurs par convention
Max_length = 100
Medium_length = 50
Min_length = 25

# Modèle de base avec des champs communs
class BaseModel(CommonAbstractModel):
    code = models.CharField('Code', max_length=Min_length, unique=True)
    label = models.CharField(max_length=Max_length, blank=True, null=True)
    description = RichTextField()  # Champ riche pour le modèle

    class Meta:
        abstract = True  # Modèle abstrait pour être réutilisé


class MailContent(CommonAbstractModel):
    is_active = models.BooleanField(default=True)
    account_activation_mail = models.TextField(
        null=True,
        blank=True,
        default="""{{phone}}\n{{link}}""",
        verbose_name="Mail d'activation de compte avec lien",
    )
    account_activation_sms = models.TextField(
        null=True,
        blank=True,
        default="""{{phone}}\n{{otp}}""",
        verbose_name="Génération d'OTP pour activation d'un compte",
    )

    class Meta:
        ordering = ["pk"]
        verbose_name = "contenu de mail"
        verbose_name_plural = "contenus de mail"
        permissions = [
            ("list_mailcontent", f"peut lister {verbose_name}"),
        ]


# UFR - Unités de Formation et de Recherche
class UniteDeRecherche(BaseModel):
    class Meta:
        ordering = ["label"]
        verbose_name = "Unité de Recherche"
        verbose_name_plural = "Unités de Recherche"
        permissions = [("list_unitederecherche", f"Peut lister {verbose_name}")]

    def __str__(self):
        return self.label

# Département rattaché à une UFR
class Departement(BaseModel):
    ufr = models.ForeignKey(UniteDeRecherche, on_delete=models.CASCADE, related_name="departement_urf")
    
    class Meta:
        ordering = ["label"]
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        permissions = [("list_departement", f"Peut lister {verbose_name}")]

    def __str__(self):
        return self.label

# Semestre rattaché à un niveau
class Semestre(BaseModel):
    class Meta:
        ordering = ["label"]
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
        permissions = [("list_semestre", f"Peut lister {verbose_name}")]
        
    def __str__(self):
        return self.label
    
# Niveau rattaché à une filière
class Niveau(BaseModel):
    semestres = models.ManyToManyField(Semestre, related_name="filiere_semestres")
    
    class Meta:
        ordering = ["label"]
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        permissions = [("list_niveau", f"Peut lister {verbose_name}")]
        
    def __str__(self):
        return self.label

# Filière rattachée à un département
class Filiere(BaseModel):
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name="filiere_department")
    niveaux = models.ManyToManyField(Niveau, related_name="filiere_niveaux")
    
    class Meta:
        ordering = ["label"]
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        permissions = [("list_filiere", f"Peut lister {verbose_name}")]

    def __str__(self):
        return self.label 

# UE (Unité d'Enseignement) rattachée à une filière
class UE(BaseModel):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name="ue_filiere")
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name="ue_niveau")
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name="ue_semestre")
    
    class Meta:
        ordering = ["label"]
        verbose_name = "Unité d'Enseignement"
        verbose_name_plural = "Unités d'Enseignement"
        permissions = [("list_ue", f"Peut lister {verbose_name}")]

    def __str__(self):
        return self.label

# Exemple de Module rattaché à un niveau
class Module(BaseModel):
    ufr = models.ForeignKey(UniteDeRecherche, on_delete=models.CASCADE, related_name="module_urf")
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name="module_department")
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name="module_filiere")
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name="module_niveau")
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name="module_semestre")
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    volume_horaire = models.IntegerField(null=True, verbose_name='volume_horaire')
    credit = models.IntegerField(null=True, verbose_name='credit')
    
    class Meta:
        ordering = ["label"]
        verbose_name = "module"
        verbose_name_plural = "modules"
        permissions = [("list_module", f"Peut lister {verbose_name}")]

    def __str__(self):
        return self.label
    


class Promotion(CommonAbstractModel):
    name = models.CharField(max_length=20, unique=True, verbose_name="Nom de la promotion")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")

    class Meta:
        ordering = ["name"]
        verbose_name = "promotion"
        verbose_name_plural = "promotions"
        permissions = [("list_module", f"Peut lister {verbose_name}")]

    def __str__(self):
        return self.name

class Annee_univ(CommonAbstractModel):
    name = models.CharField(max_length=20, unique=True, verbose_name="Année universitaire")
    start_date = models.DateField(verbose_name="Début")
    end_date = models.DateField(verbose_name="Fin")

    class Meta:
        ordering = ["name"]
        verbose_name = "annee_univ"
        verbose_name_plural = "annee_univs"
        permissions = [("list_module", f"Peut lister {verbose_name}")]

    def __str__(self):
        return self.name
    


