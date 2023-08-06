import pdb

from django.contrib import admin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django_audit_fields.admin import audit_fieldset_tuple
from edc_dashboard.url_names import url_names
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import mocca_screening_admin
from ..eligibility import format_reasons_ineligible
from ..forms import SubjectScreeningForm
from ..models import SubjectScreening


class MyAutocompleteJsonView(AutocompleteJsonView):
    def get_queryset(self):
        """Return queryset based on ModelAdmin.get_search_results()."""
        pdb.set_trace()
        qs = self.model_admin.get_queryset(self.request)
        qs, search_use_distinct = self.model_admin.get_search_results(
            self.request, qs, self.term
        )
        if search_use_distinct:
            qs = qs.distinct()
        return qs.filter(mocca_register__screening_identifier__isnull=True)


@admin.register(SubjectScreening, site=mocca_screening_admin)
class SubjectScreeningAdmin(ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin):
    form = SubjectScreeningForm

    post_url_on_delete_name = "screening_listboard_url"
    subject_listboard_url_name = "screening_listboard_url"

    additional_instructions = (
        "Patients must meet ALL of the inclusion criteria and NONE of the "
        "exclusion criteria in order to proceed to the final screening stage"
    )

    autocomplete_fields = ["mocca_register"]

    fieldsets = (
        [None, {"fields": ("screening_consent", "report_datetime")}],
        ["Inclusion Criteria", {"fields": ("mocca_participant",)}],
        ["Original MOCCA information", {"fields": ("mocca_register",)}],
        audit_fieldset_tuple,
    )

    list_display = (
        "screening_identifier",
        "eligiblity_status",
        "demographics",
        "reasons",
        "report_datetime",
        "user_created",
        "created",
    )

    list_filter = (
        "report_datetime",
        "gender",
        "eligible",
        "consented",
        "refused",
        "eligible",
    )

    search_fields = (
        "screening_identifier",
        "subject_identifier",
        "mocca_study_identifier",
        "mocca_screening_identifier",
        "initials",
        "reasons_ineligible",
    )

    radio_fields = {
        "mocca_participant": admin.VERTICAL,
        "mocca_site": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "screening_consent": admin.VERTICAL,
        "unsuitable_agreed": admin.VERTICAL,
        "unsuitable_for_study": admin.VERTICAL,
    }

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj=obj)
        if obj and "mocca_register" not in fields:
            fields.append("mocca_register")
        return fields

    def post_url_on_delete_kwargs(self, request, obj):
        return {}

    def demographics(self, obj=None):
        return mark_safe(
            f"{obj.get_gender_display()} {obj.age_in_years}yrs {obj.initials.upper()}"
        )

    def reasons(self, obj=None):
        return format_reasons_ineligible(obj.reasons_ineligible)

    def eligiblity_status(self, obj=None):
        return "Eligible" if obj.eligible else "Ineligible"

    def dashboard(self, obj=None, label=None):
        try:
            url = reverse(
                self.get_subject_dashboard_url_name(),
                kwargs=self.get_subject_dashboard_url_kwargs(obj),
            )
        except NoReverseMatch:
            url = reverse(url_names.get("screening_listboard_url"), kwargs={})
            context = dict(
                title=_("Go to screening listboard"),
                url=f"{url}?q={obj.screening_identifier}",
                label=label,
            )
        else:
            context = dict(title=_("Go to subject dashboard"), url=url, label=label)
        return render_to_string("dashboard_button.html", context=context)

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "mocca_register":
    #         kwargs["queryset"] = db_field.related_model.objects.filter(
    #             screening_identifier__isnull=True
    #         ).order_by("mocca_study_identifier")
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super().get_search_results(
    #         request, queryset, search_term
    #     )
    #     path = urlsplit(request.META.get("HTTP_REFERER")).path
    #     query = urlsplit(request.META.get("HTTP_REFERER")).query
    #     if "bloodresult" in path or "lumbarpuncturecsf" in path:
    #         attrs = parse_qs(query)
    #         try:
    #             subject_visit = attrs.get("subject_visit")[0]
    #         except IndexError:
    #             pass
    #         else:
    #             queryset = queryset.filter(
    #                 subject_visit__id=subject_visit, is_drawn=YES
    #             )
    #     return queryset, use_distinct

    def autocomplete_view(self, request):
        return AutocompleteJsonView.as_view(model_admin=self)(request)
