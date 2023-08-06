from django import forms
from edc_constants.constants import ALIVE, UNKNOWN, YES
from edc_form_validators import FormValidator, FormValidatorMixin

from ..models import MoccaRegisterContact


class MoccaRegisterContactFormValidator(FormValidator):
    def clean(self):
        self.applicable_if(YES, field="answered", field_applicable="respondent")
        self.applicable_if(YES, field="answered", field_applicable="survival_status")
        self.not_applicable(
            UNKNOWN,
            ALIVE,
            field="survival_status",
            field_applicable="death_date",
            inverse=False,
        )
        self.applicable_if(YES, field="answered", field_applicable="willing_to_attend")
        self.required_if(YES, field="attends_facility", field_required="next_appt_date")


class MoccaRegisterContactForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = MoccaRegisterContactFormValidator

    class Meta:
        model = MoccaRegisterContact
        fields = [
            "answered",
            "respondent",
            "survival_status",
            "death_date",
            "willing_to_attend",
            "icc",
            "next_appt_date",
            "call_again",
            "report_datetime",
        ]
        labels = {"report_datetime": "Date", "answered": "Did someone answer?"}
