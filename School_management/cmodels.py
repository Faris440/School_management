from django.db import models
from django.contrib.auth.models import User
from model_utils.models import (
    TimeStampedModel,
    UUIDModel,
    SoftDeletableModel,
    StatusModel,
)
from model_utils.choices import Choices
from autoslug import AutoSlugField


from School_management.constants import LONG_LENGTH, MEDIUM_LENGTH, MIN_LENGTH

CONSTRAINT = models.PROTECT


class CommonAbstractModel(TimeStampedModel, UUIDModel, SoftDeletableModel):
    is_active = models.BooleanField("Est actif", default=True)
    class Meta:
        abstract = True




