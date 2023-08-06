from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin

from ..models import SubjectScreening


class SubjectScreeningFormValidator(FormValidator):
    def clean(self):
        if (
            not self.cleaned_data.get("screening_consent")
            or self.cleaned_data.get("screening_consent") != YES
        ):
            raise forms.ValidationError(
                {
                    "screening_consent": (
                        "You may NOT screen this subject without their verbal consent."
                    )
                }
            )
        if self.cleaned_data.get("mocca_participant") != YES:
            raise forms.ValidationError(
                {
                    "mocca_participant": (
                        "Subject must have been a participant in the original MOCCA trial."
                    )
                }
            )

        self.validate_mocca_study_identifier_with_site()

        if (
            self.cleaned_data.get("age_in_years")
            and self.cleaned_data.get("age_in_years") < 18
        ):
            raise forms.ValidationError(
                {"age_in_years": "Participant must be at least 18 years old."}
            )

        self.validate_mocca_enrollment_data()

        self.required_if(
            YES, field="unsuitable_for_study", field_required="reasons_unsuitable"
        )

        self.applicable_if(
            YES, field="unsuitable_for_study", field_applicable="unsuitable_agreed"
        )

        if self.cleaned_data.get("unsuitable_agreed") == NO:
            raise forms.ValidationError(
                {
                    "unsuitable_agreed": (
                        "The study coordinator MUST agree with your assessment. "
                        "Please discuss before continuing."
                    )
                }
            )

    def validate_mocca_study_identifier_with_site(self):
        mocca_register = None
        mocca_register_cls = django_apps.get_model("mocca_screening.moccaregister")
        if self.cleaned_data.get("mocca_study_identifier") and self.cleaned_data.get(
            "mocca_site"
        ):
            try:
                mocca_register = mocca_register_cls.objects.get(
                    mocca_study_identifier=self.cleaned_data.get(
                        "mocca_study_identifier"
                    ),
                )
            except ObjectDoesNotExist:
                raise forms.ValidationError(
                    {
                        "mocca_study_identifier": (
                            "Invalid MOCCA (original) study identifier."
                        )
                    }
                )
            else:
                if mocca_register.mocca_site != self.cleaned_data.get("mocca_site"):
                    raise forms.ValidationError(
                        {
                            "mocca_site": "Invalid MOCCA (original) site for given study identifier."
                        }
                    )
        return mocca_register

    def validate_mocca_enrollment_data(self):
        """Raises an exception if either the birth year or initials
        do not match the register record for the given
        `mocca_study_identifier`.
        """
        mocca_register = self.validate_mocca_study_identifier_with_site()
        if (
            mocca_register
            and self.cleaned_data.get("birth_year")
            and self.cleaned_data.get("initials")
        ):
            for attrname in ["initials", "gender", "birth_year"]:
                if getattr(mocca_register, attrname) != self.cleaned_data.get(attrname):
                    label = attrname.replace("_", " ")
                    raise forms.ValidationError(
                        {
                            attrname: (
                                f"Invalid {label} for this MOCCA (original) study identifier."
                            )
                        }
                    )

        if (
            self.cleaned_data.get("age_in_years")
            and self.cleaned_data.get("birth_year")
            and self.cleaned_data.get("report_datetime")
        ):
            expected_age = self.cleaned_data.get(
                "report_datetime"
            ).year - self.cleaned_data.get("birth_year")
            if abs(expected_age - self.cleaned_data.get("age_in_years")) > 1:
                raise forms.ValidationError(
                    {"age_in_years": "Does not make sense relative to birth year given"}
                )


class SubjectScreeningForm(
    AlreadyConsentedFormMixin, FormValidatorMixin, forms.ModelForm
):
    form_validator_cls = SubjectScreeningFormValidator

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = SubjectScreening
        fields = [
            "screening_consent",
            "report_datetime",
            "mocca_participant",
            "mocca_site",
            "mocca_study_identifier",
            "initials",
            "gender",
            "birth_year",
            "age_in_years",
            "unsuitable_for_study",
            "reasons_unsuitable",
            "unsuitable_agreed",
        ]
