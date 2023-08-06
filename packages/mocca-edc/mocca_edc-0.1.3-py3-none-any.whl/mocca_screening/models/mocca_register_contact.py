from django.db import models
from edc_constants.choices import (
    ALIVE_DEAD_UNKNOWN_NA,
    YES_NO,
    YES_NO_UNSURE_NA,
)
from edc_constants.constants import NO, NOT_APPLICABLE
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from ..choices import RESPONDENT_CHOICES
from .mocca_register import MoccaRegister


class Manager(models.Manager):
    """A manager class for Crf models, models that have an FK to
    the visit model.
    """

    use_in_migrations = True

    def get_by_natural_key(self, mocca_register):
        return self.get(mocca_register=mocca_register)


class MoccaRegisterContact(SiteModelMixin, BaseUuidModel):

    mocca_register = models.ForeignKey(MoccaRegister, on_delete=models.PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)

    answered = models.CharField(max_length=15, choices=YES_NO, default=NO)

    respondent = models.CharField(
        max_length=15, choices=RESPONDENT_CHOICES, default=NOT_APPLICABLE
    )

    survival_status = models.CharField(
        max_length=15, choices=ALIVE_DEAD_UNKNOWN_NA, default=NOT_APPLICABLE
    )

    willing_to_attend = models.CharField(
        max_length=15, choices=YES_NO_UNSURE_NA, default=NOT_APPLICABLE
    )

    call_again = models.CharField(
        verbose_name="Try again?", max_length=15, choices=YES_NO
    )

    on_site = CurrentSiteManager()
    objects = Manager()
    history = HistoricalRecords()

    def __str__(self):
        return str(self.mocca_register)

    def natural_key(self):
        return (self.mocca_register,)

    natural_key.dependencies = [
        "sites.Site",
        "mocca_screening.MoccaRegister",
    ]

    class Meta:
        verbose_name = "MOCCA Patient Register Contact"
        verbose_name_plural = "MOCCA Patient Register Contacts"
