from django import forms
from edc_constants.constants import YES
from edc_form_validators import FormValidator, FormValidatorMixin

from ..models import MoccaRegisterContact


class MoccaRegisterContactFormValidator(FormValidator):
    def clean(self):
        self.applicable_if(YES, field="answered", field_applicable="respondent")
        self.applicable_if(YES, field="answered", field_applicable="survival_status")
        self.applicable_if(YES, field="answered", field_applicable="willing_to_attend")


class MoccaRegisterContactForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = MoccaRegisterContactFormValidator

    class Meta:
        model = MoccaRegisterContact
        fields = [
            "answered",
            "respondent",
            "survival_status",
            "willing_to_attend",
            "call_again",
            "report_datetime",
        ]
        labels = {"report_datetime": "Date"}
