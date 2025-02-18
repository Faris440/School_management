from django.db import models
from School_management.cmodels import CONSTRAINT, CommonAbstractModel
import uuid
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField

from School_management.constants import MEDIUM_LENGTH

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

# Niveau rattaché à une filière
class Niveau(BaseModel):
    class Meta:
        ordering = ["label"]
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        permissions = [("list_niveau", f"Peut lister {verbose_name}")]
        
    def __str__(self):
        return self.label

# Semestre rattaché à un niveau
class Semestre(BaseModel):
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name="semestre_niveau")
    class Meta:
        ordering = ["label"]
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
        permissions = [("list_semestre", f"Peut lister {verbose_name}")]
        
    def __str__(self):
        return self.label


    
# Filière rattachée à un département
class Filiere(BaseModel):
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name="filiere_department")
    class Meta:
        ordering = ["label"]
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        permissions = [("list_filiere", f"Peut lister {verbose_name}")]

    def __str__(self):
        return f"{self.label}"
    
# UE (Unité d'Enseignement) rattachée à une filière
class UE(BaseModel):
    filiere = models.ForeignKey(
        Filiere, 
        on_delete=models.CASCADE, 
        related_name="ue_filiere"
    )
    ufr = models.ForeignKey(
        "parameter.UniteDeRecherche", 
        on_delete=models.CASCADE, 
        related_name="ue",
        null=True,
        blank=True,
        verbose_name="UFR"
    )
    departement = models.ForeignKey(
        "parameter.Departement", 
        on_delete=models.CASCADE, 
        related_name="ue",
        null=True,
        blank=True,
        verbose_name="Département"
    )
    niveau = models.ForeignKey(
        "parameter.Niveau", 
        on_delete=models.CASCADE, 
        related_name="ue",
        null=True,
        blank=True,
        verbose_name="Niveau"
    )
    semestre = models.ForeignKey(
        "parameter.Semestre", 
        on_delete=models.CASCADE, 
        related_name="ue",
        null=True,
        blank=True,
        verbose_name="Semestre"
    )
    
    class Meta:
        ordering = ["label"]
        verbose_name = "Unité d'Enseignement"
        verbose_name_plural = "Unités d'Enseignement"
        permissions = [("list_ue", f"Peut lister {verbose_name}")]

    def save(self, *args, **kwargs):
        """
        Lors de l'enregistrement du module, assigner automatiquement
        l'UFR et le Département à partir de la Filière.
        """
        if self.filiere:
            self.departement = self.filiere.departement
            if self.filiere.departement:
                self.ufr = self.filiere.departement.ufr
        
        # Suppression de la condition self.ue, car elle n'est pas définie dans ce modèle.
        # Si vous souhaitez affecter le niveau et le semestre en fonction de la filière, vous pouvez faire :
        if self.filiere and not self.niveau:
            self.niveau = self.filiere.niveau  # Ajustez selon la logique de votre modèle.
        if self.filiere and not self.semestre:
            self.semestre = self.filiere.semestre  # Ajustez selon la logique de votre modèle.

        super().save(*args, **kwargs)

    def __str__(self):
        return self.label

class Volume_horaire(CommonAbstractModel):
    # label = models.CharField(max_length=255, verbose_name="Nom du volume horaire")
    heures = models.PositiveIntegerField("Volume horaire (en heures)")

    class Meta:
        ordering = ["heures"]
        verbose_name = "volumeHoraire"
        verbose_name_plural = "volumeHoraires"
        permissions = [("list_volume_horaire", "Peut lister volumeHoraire")]

    def __str__(self):
        return f"{self.heures} ({self.heures} heures)"
    
    def clean(self):
        """
        Valide les contraintes sur le champ `heures`.
        """
        # Vérifier que `heures` est un multiple de 12
        if self.heures % 12 != 0:
            raise ValidationError("Le volume horaire doit être un multiple de 12.")
        
        # Vérifier que `heures` est supérieur ou égal à 12
        if self.heures < 12:
            raise ValidationError("Le volume horaire doit être au moins égal à 12 heures.")
        
        # Optionnel : Limiter la plage des heures si nécessaire
        if self.heures > 120:
            raise ValidationError("Le volume horaire ne peut pas dépasser 120 heures.")

    @property
    def calcul_credits(self):
        """
        Calcule le nombre de crédits en fonction du volume horaire.
        """
        return self.heures // 12

    def save(self, *args, **kwargs):
        """
        Vérifie les validations avant d'enregistrer.
        """
        self.clean()
        super().save(*args, **kwargs)

# Exemple de Module rattaché à un niveau
class Module(BaseModel):
    cours_theorique = models.IntegerField("Volume horaire cours théorique", default=0)
    travaux_pratiques = models.IntegerField("Volume horaire travaux tratiques", default=0)
    travaux_diriges = models.IntegerField("Volume horaire travaux dirigés", default=0)

    filiere= models.ForeignKey(
        Filiere, 
        on_delete=models.CASCADE, 
        related_name="module_filiere"
    )
    ue = models.ForeignKey(
        UE, 
        on_delete=models.CASCADE,
        related_name="module_filiere"
    )
    ufr = models.ForeignKey(
        "parameter.UniteDeRecherche", 
        on_delete=models.CASCADE, 
        related_name="modules",
        null=True,
        blank=True,
        verbose_name="UFR"
    )
    departement = models.ForeignKey(
        "parameter.Departement", 
        on_delete=models.CASCADE, 
        related_name="modules",
        null=True,
        blank=True,
        verbose_name="Département"
    )
    niveau = models.ForeignKey(
        "parameter.Niveau", 
        on_delete=models.CASCADE, 
        related_name="modules",
        null=True,
        blank=True,
        verbose_name="Niveau"
    )
    semestre = models.ForeignKey(
        "parameter.Semestre", 
        on_delete=models.CASCADE, 
        related_name="modules",
        null=True,
        blank=True,
        verbose_name="Semestre"
    )
    
    volume_horaire =models.ForeignKey(
        Volume_horaire, 
        on_delete=models.CASCADE, 
        null=True,
        blank=True,
        related_name="module_volume_horaire",
        verbose_name="Volume horaire"

    )
    credit = models.IntegerField(
        default=0,
        verbose_name="Crédit"
    )
    

    class Meta:
        ordering = ["label"]
        verbose_name = "module"
        verbose_name_plural = "modules"
        permissions = [("list_module", f"Peut lister {verbose_name}")]

    def save(self, *args, **kwargs):
        """
        Lors de l'enregistrement du module, assigner automatiquement
        l'UFR et le Département à partir de la Filière.
        """
        if self.filiere:
            self.departement = self.filiere.departement
            if self.filiere.departement:
                self.ufr = self.filiere.departement.ufr
        if self.ue:
            self.niveau = self.ue.niveau
            self.semestre = self.ue.semestre

        super().save(*args, **kwargs)

    def __str__(self):
        
        return f"{self.label} - {self.niveau}-{self.semestre} ({self.filiere}) "
    
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
    
class Promotion(CommonAbstractModel):
    filiere = models.ManyToManyField(Filiere, related_name="promotion_filiere")
    name = models.CharField(max_length=20, unique=True, verbose_name="Nom de la promotion")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")

    class Meta:
        ordering = ["name"]
        verbose_name = "promotion"
        verbose_name_plural = "promotions"
        permissions = [("list_promotion", f"Peut lister {verbose_name}")]

    def __str__(self):
        return self.name

    
class Credit(CommonAbstractModel):
    volume_horaire = models.OneToOneField(Volume_horaire, on_delete=models.CASCADE, related_name="credit")
    valeur = models.PositiveIntegerField("Valeur du crédit", editable=False)

    def save(self, *args, **kwargs):
        """
        Calcule et met à jour la valeur du crédit en fonction du volume horaire.
        """
        self.valeur = self.volume_horaire.calcul_credits
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.valeur} crédits pour {self.volume_horaire}"


class Grade(BaseModel):
    class Meta:
        ordering = ["label"]
        verbose_name = "grade"
        verbose_name_plural = "grades"
        permissions = [("list_Grade", f"Peut lister {verbose_name}")]

    def __str__(self):
        return self.label
