from django.db import models
from School_management.cmodels import CONSTRAINT, CommonAbstractModel
from School_management.constants import BIG_LENGTH


 # Définitions des longueurs par convention
Max_length = 100
Medium_length = 50
Min_length = 25
# Create your models here.
class Sheet(CommonAbstractModel):
    enseignant = models.ForeignKey("xauth.User", on_delete=models.CASCADE, related_name="sheet_enseignant")
    etablissement_enseigne = models.CharField(max_length= BIG_LENGTH, verbose_name="Etablissement enseigné",null=True) 
    volume_horaire_statuaire = models.IntegerField(null=True, verbose_name='Volume horaire statuaire')
    abattement = models.IntegerField(null=True, verbose_name='veuillez saisir l\'abattement')
    motif_abattement = models.CharField(max_length= BIG_LENGTH, verbose_name="Motif de l'abattement",null=True) 
    v_h_obli_apres_abattement = models.IntegerField(null=True, verbose_name='Volume horaire après abattement')
    date_debut = models.DateField(auto_now=False, auto_now_add=False,null=False, verbose_name="Date de début du cours")
    date_fin = models.DateField(auto_now=False, auto_now_add=False,null=False, verbose_name="Date de fin du cours")
    is_validated = models.BooleanField(null=True, verbose_name="Validé")
    motif_de_rejet = models.CharField(max_length= BIG_LENGTH, verbose_name="motif_refus",null=True)
    is_permanent = models.BooleanField(null=True, verbose_name="type_fiche_permanent")
    filiere = models.ForeignKey("parameter.Filiere",on_delete=models.CASCADE,related_name="sheet_filiere", verbose_name="Filière consernée")

    validate_by_responsable_filiere = models.BooleanField(null=True)
    validate_by_responsable_ufr = models.BooleanField(null=True)
    validate_by_vice_presient = models.BooleanField(null=True)

    def __str__(self):
        return self.enseignant
    
    def check_sheet(self):
        enseignements = self.enseignement_sheet.all()
        status = None
        for enseignement in enseignements:
            if enseignement.validate_by_responsable_filiere is None:
                status = True
            elif enseignement.validate_by_vice_presient is not None or enseignement.validate_by_responsable_ufr is False or enseignement.validate_by_responsable_filiere is False:
                return False
        return status
    
    class Meta:
        ordering = ["-created"]
        verbose_name = "Fiche"
        verbose_name_plural = "Fiches"
        permissions = [("list_fiche", f"Peut lister {verbose_name}"),
                       ("can_valide_sheet", f"Peut valider {verbose_name}"),
                       ("can_invalide_sheet", f"Peut invalider {verbose_name}"),
                       ("can_add_multiple_sheet", f"Peut soumettre un formulaire pour enseignant {verbose_name}"),
                       
                       ]
        
    
class Enseignements(CommonAbstractModel):
    code = models.CharField('code',null=True, max_length=Min_length, unique=True)
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, related_name="enseignement_sheet")
    niveau = models.ForeignKey("parameter.Niveau",on_delete=models.CASCADE,related_name="sheet_niveau", verbose_name="Niveau de la filière")
    semestre = models.ForeignKey("parameter.Semestre",on_delete=models.CASCADE,related_name="sheet_semestre", verbose_name="Semestre du cours")
    module = models.ForeignKey("parameter.Module",on_delete=models.CASCADE,related_name="sheet_module", verbose_name="Module enseigné")

    ct_volume_horaire_confie = models.IntegerField(null=False, verbose_name='Volume_horaire confié, CT')
    td_volume_horaire_confie = models.IntegerField(null=False, verbose_name='Volume_horaire confié, TD')
    tp_volume_horaire_confie = models.IntegerField(null=False, verbose_name='Volume_horaire confié, TP')
    ct_volume_horaire_efectue = models.IntegerField(null=False, verbose_name='Volume horaire éffectué, CT')
    td_volume_horaire_efectue = models.IntegerField(null=False, verbose_name='Volume horaire éffectué, TD')
    tp_volume_horaire_efectue = models.IntegerField(null=False, verbose_name='Volume horaire éffectué, TP')
    is_validated = models.BooleanField(null=True, verbose_name="Validé")
    motif_de_rejet = models.CharField(max_length= BIG_LENGTH, verbose_name="motif_refus",null=True)
    
    validate_by_responsable_filiere = models.BooleanField(null=True)
    validate_by_responsable_ufr = models.BooleanField(null=True)
    validate_by_vice_presient = models.BooleanField(null=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Enseignement"
        verbose_name_plural = "Enseignements"
        permissions = [("list_enseignement", f"Peut lister {verbose_name}")]
        
    def __str__(self):
        return self.module.label
    