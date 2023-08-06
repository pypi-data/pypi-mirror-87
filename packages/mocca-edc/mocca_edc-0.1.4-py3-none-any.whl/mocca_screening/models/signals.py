from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from edc_constants.constants import NO

from .mocca_register_contact import MoccaRegisterContact
from .subject_refusal import SubjectRefusal
from .subject_screening import SubjectScreening


@receiver(
    post_save,
    weak=False,
    sender=SubjectScreening,
    dispatch_uid="subject_screening_on_post_save",
)
def subject_screening_on_post_save(sender, instance, raw, created, **kwargs):
    """Updates `mocca_register` patient as used / screened
    """
    if not raw:
        instance.mocca_register.screening_identifier = instance.screening_identifier
        instance.mocca_register.call = NO
        instance.mocca_register.save(update_fields=["call", "screening_identifier"])


@receiver(
    post_save,
    weak=False,
    sender=MoccaRegisterContact,
    dispatch_uid="mocca_register_contact_on_post_save",
)
def mocca_register_contact_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        qs = sender.objects.filter(mocca_register=instance.mocca_register)
        instance.mocca_register.contact_attempts = qs.count()
        last_obj = qs.last()
        instance.mocca_register.call = last_obj.call_again
        instance.mocca_register.date_last_called = last_obj.report_datetime.date()
        if last_obj.next_appt_date:
            instance.mocca_register.next_appt_date = last_obj.next_appt_date
        if instance.mocca_register.screening_identifier:
            instance.mocca_register.call = NO
        instance.mocca_register.save(
            update_fields=[
                "call",
                "contact_attempts",
                "date_last_called",
                "next_appt_date",
            ]
        )


@receiver(
    post_save,
    weak=False,
    sender=SubjectRefusal,
    dispatch_uid="subject_refusal_on_post_save",
)
def subject_refusal_on_post_save(sender, instance, raw, created, **kwargs):
    """Updates `refused` field on SUbjectScreening
    """
    if not raw:
        try:
            obj = SubjectScreening.objects.get(
                screening_identifier=instance.screening_identifier
            )
        except ObjectDoesNotExist:
            pass
        else:
            obj.refused = True
            obj.save(update_fields=["refused"])


@receiver(
    post_delete,
    weak=False,
    sender=SubjectRefusal,
    dispatch_uid="subject_refusal_on_post_delete",
)
def subject_refusal_on_post_delete(sender, instance, using, **kwargs):
    """Updates/Resets subject screening.
    """
    try:
        obj = SubjectScreening.objects.get(
            screening_identifier=instance.screening_identifier
        )
    except ObjectDoesNotExist:
        pass
    else:
        obj.refused = False
        obj.save(update_fields=["refused"])
