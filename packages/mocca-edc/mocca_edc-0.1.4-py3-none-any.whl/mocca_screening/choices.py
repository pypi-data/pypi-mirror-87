from edc_constants.constants import (
    NO,
    NOT_APPLICABLE,
    OTHER,
    DIABETES,
    HIV,
    HYPERTENSION,
    PURPOSIVELY_SELECTED,
    RANDOM_SAMPLING,
    UNKNOWN,
)

from .constants import (
    DIABETES_CLINIC,
    HIV_CLINIC,
    HYPERTENSION_CLINIC,
    INTEGRATED,
    NCD,
    NCD_CLINIC,
    NO_INTERRUPTION,
    SOME_INTERRUPTION,
    SEQUENTIAL,
    SYSTEMATIC,
)

CLINIC_CHOICES = (
    (HIV_CLINIC, "HIV Clinic"),
    (NCD_CLINIC, "NCD Clinic (Joint Diabetes/Hypertension)"),
    (DIABETES_CLINIC, "Diabetes Clinic"),
    (HYPERTENSION_CLINIC, "Hypertension Clinic"),
    (INTEGRATED, "Integrated Clinic"),
)

REFUSAL_REASONS = (
    ("unwilling_to_say", "I am unwilling to say"),
    ("dont_have_time", "I don't have time"),
    ("stigma", "I am worried about stigma"),
    ("must_consult_spouse", "I need to consult my spouse"),
    ("dont_want_medication", "I don't want to take any more medication"),
    ("dont_want_to_join", "I don't want to take part"),
    ("need_to_think_about_it", "I haven't had a chance to think about it"),
    ("moving", "I am moving to another area"),
    (OTHER, "Other, please specify"),
)


CLINIC_DAYS = (
    (INTEGRATED, "Integrated care day (HIV, Diabetes, Hypertension)"),
    (NCD, "NCD day (Diabetes + Hypertension)"),
    (HIV, "HIV only day"),
    (DIABETES, "Diabetes only day"),
    (HYPERTENSION, "Hypertension only day"),
)

SELECTION_METHOD = (
    (RANDOM_SAMPLING, "Random sampling"),
    (SYSTEMATIC, "Systematically selected"),
    (SEQUENTIAL, "Sequentially selected"),
    (PURPOSIVELY_SELECTED, "Purposively selected"),
)

RESPONDENT_CHOICES = (
    ("patient", "Patient"),
    ("family", "Family"),
    ("friend", "friend"),
    ("other", "other"),
    (NOT_APPLICABLE, "Not applicable"),
)

CARE_SINCE_MOCCA = (
    (NO_INTERRUPTION, "Yes, without interruption"),
    (SOME_INTERRUPTION, "Yes, with some interruption"),
    (NO, "No, not since completing follow up with the MOCCA (original) trial."),
    (UNKNOWN, "Unknown"),
)

NOT_ICC_REASONS = (
    ("icc_not_available", "ICC not available (or closed) in this facility"),
    ("moved", "Moved out of area"),
    ("dont_want", "Personally chose not to continue with integrated care"),
    (
        "advised_to_vertical",
        "Healthcare staff asked patient to return to vertical care",
    ),
    ("referred_out", "Referred to another facility without an ICC"),
    (NOT_APPLICABLE, "Not applicable"),
)
