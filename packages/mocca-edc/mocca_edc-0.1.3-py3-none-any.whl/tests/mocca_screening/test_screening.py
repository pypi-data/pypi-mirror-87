import pdb

from django.test import TestCase, tag
from edc_constants.constants import (
    FEMALE,
    MALE,
    YES,
    NO,
    NOT_APPLICABLE,
)
from edc_sites import get_current_country
from edc_utils.date import get_utcnow
from mocca_lists.models import MoccaOriginalSites
from mocca_screening.constants import INTEGRATED
from mocca_screening.forms import SubjectScreeningForm
from mocca_screening.import_mocca_register import import_mocca_register
from mocca_screening.mocca_original_sites import get_mocca_sites_by_country
from mocca_screening.models import MoccaRegister, SubjectScreening

from ..mocca_test_case_mixin import MoccaTestCaseMixin


class TestForms(MoccaTestCaseMixin, TestCase):
    def setUp(self):
        self.mocca_register = MoccaRegister.objects.filter(
            mocca_country=get_current_country()
        )[0]
        self.mocca_site = MoccaOriginalSites.objects.get(
            name=self.mocca_register.mocca_site.name
        )
        self.sites = get_mocca_sites_by_country(country=get_current_country())

    def get_data(self):
        return {
            "screening_consent": YES,
            "report_datetime": get_utcnow(),
            "mocca_participant": YES,
            "mocca_site": str(self.mocca_site.id),
            "mocca_study_identifier": self.mocca_register.mocca_study_identifier,
            "initials": self.mocca_register.initials,
            "gender": self.mocca_register.gender,
            "birth_year": self.mocca_register.birth_year,
            "age_in_years": self.mocca_register.age_in_years,
            "clinic_type": INTEGRATED,
            "unsuitable_for_study": NO,
            "unsuitable_agreed": NOT_APPLICABLE,
        }

    @tag("123")
    def test_screening_ok(self):
        form = SubjectScreeningForm(data=self.get_data(), instance=None)
        form.is_valid()
        self.assertEqual(form._errors, {})
        form.save()
        self.assertTrue(SubjectScreening.objects.all()[0].eligible)

    @tag("123")
    def test_screening_no_matching_site(self):
        data = self.get_data()
        sites = {k: v for k, v in self.sites.items() if v.name != self.mocca_site.name}
        mocca_site = MoccaOriginalSites.objects.get(name=list(sites)[0])
        data.update(mocca_site=mocca_site)
        form = SubjectScreeningForm(data=data, instance=None)
        form.is_valid()
        self.assertIn("mocca_site", form._errors)

    @tag("123")
    def test_screening_no_matching_study_identifier(self):
        data = self.get_data()
        data.update(mocca_study_identifier="1111111")
        form = SubjectScreeningForm(data=data, instance=None)
        form.is_valid()
        self.assertIn("mocca_study_identifier", form._errors)

    @tag("123")
    def test_screening_no_matching_gender(self):
        data = self.get_data()
        data.update(gender=FEMALE if data.get("gender") == MALE else MALE)
        form = SubjectScreeningForm(data=data, instance=None)
        form.is_valid()
        self.assertIn("gender", form._errors)

    @tag("123")
    def test_screening_no_matching_initials(self):
        data = self.get_data()
        data.update(initials="XX")
        form = SubjectScreeningForm(data=data, instance=None)
        form.is_valid()
        self.assertIn("initials", form._errors)

    @tag("123")
    def test_screening_no_matching_birth_year(self):
        data = self.get_data()
        data.update(birth_year=1901)
        form = SubjectScreeningForm(data=data, instance=None)
        form.is_valid()
        self.assertIn("birth_year", form._errors)

    def test_screening_invalid(self):

        data = self.get_data()

        responses = dict(age_in_years=17,)

        for k, v in responses.items():
            with self.subTest(k=v):
                data.update({k: v})
                form = SubjectScreeningForm(data=data, instance=None)
                form.is_valid()
                self.assertIn("age_in_years", form._errors)

    def test_screening_ineligible(self):

        data = self.get_data()

        responses = dict(
            qualifying_condition=NO, lives_nearby=NO, requires_acute_care=YES,
        )

        for k, v in responses.items():
            with self.subTest(k=v):
                data.update({k: v})
                form = SubjectScreeningForm(data=data, instance=None)
                form.is_valid()
                self.assertEqual(form._errors, {})
                form.save()

                self.assertFalse(SubjectScreening.objects.all()[0].eligible)

    def test_screening_unsuitable(self):

        data = self.get_data()

        data.update(unsuitable_for_study=YES)
        form = SubjectScreeningForm(data=data, instance=None)
        form.is_valid()
        self.assertIn("reasons_unsuitable", form._errors)

        data.update(reasons_unsuitable="blah blah")
        form = SubjectScreeningForm(data=data, instance=None)
        form.is_valid()
        self.assertIn("unsuitable_agreed", form._errors)

        data.update(unsuitable_agreed=NO)
        form = SubjectScreeningForm(data=data, instance=None)
        form.is_valid()
        self.assertIn("unsuitable_agreed", form._errors)

        data.update(unsuitable_agreed=YES)
        form = SubjectScreeningForm(data=data, instance=None)
        form.is_valid()
        form.save()
        self.assertFalse(SubjectScreening.objects.all()[0].eligible)

    @tag("123")
    def test_import_mocca_register(self):
        import_mocca_register()
