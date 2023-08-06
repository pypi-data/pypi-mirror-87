from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from edc_constants.constants import YES
from edc_utils.date import get_utcnow


def check_eligible_final(obj):
    """Updates model instance fields `eligible` and `reasons_ineligible`.
    """
    obj.eligible = get_eligible_final(obj)
    obj.reasons_ineligible = get_reasons_ineligible(obj)
    obj.eligibility_datetime = get_utcnow()


def get_eligible_final(obj):
    """Returns True or False"""
    try:
        obj.mocca_register = get_mocca_register(obj)
    except ObjectDoesNotExist:
        obj.mocca_register = None
    if obj.unsuitable_for_study == YES:
        eligible = False
    else:
        if obj.mocca_register:
            eligible = True
    return eligible


def get_reasons_ineligible(obj):
    if obj.eligible:
        reasons_ineligible = None
    else:
        reasons_ineligible = []
        if obj.unsuitable_for_study == YES:
            reasons_ineligible.append("Subject unsuitable")
        if not obj.mocca_register:
            reasons_ineligible.append("Unable to link to MOCCA (original) participant")
    return reasons_ineligible


def get_mocca_register(obj):
    opts = dict(
        mocca_study_identifier=obj.mocca_study_identifier,
        mocca_site=obj.mocca_site,
        gender=obj.gender,
        birth_year=obj.birth_year,
        initials=obj.initials,
    )
    mocca_register_cls = django_apps.get_model("mocca_screening.moccaregister")
    return mocca_register_cls.objects.get(**opts)


def format_reasons_ineligible(*str_values):
    reasons = None
    str_values = [x for x in str_values if x is not None]
    if str_values:
        str_values = "".join(str_values)
        reasons = mark_safe(str_values.replace("|", "<BR>"))
    return reasons


def eligibility_display_label(obj):
    return "ELIGIBLE" if obj.eligible else "not eligible"
