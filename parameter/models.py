from django.db import models
from School_management.cmodels import CONSTRAINT, CommonAbstractModel

# Définitions des longueurs par convention
Max_length = 100
Medium_length = 50
Min_length = 25

# Modèle de base avec des champs communs
class BaseModel(CommonAbstractModel):
    code = models.CharField('code', max_length=Min_length, unique=True)
    label = models.CharField(max_length=Max_length, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        abstract = True  # Modèle abstrait pour être réutilisé

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
