from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin import (
    ModelAdminFormInstructionsMixin,
    TabularInlineMixin,
    TemplatesModelAdminMixin,
)
from edc_model_admin.model_admin_simple_history import SimpleHistoryAdmin
from edc_sites import get_current_country
from mocca_screening.mocca_original_sites import get_mocca_sites_by_country

from ..admin_site import mocca_screening_admin
from ..forms import MoccaRegisterForm, MoccaRegisterContactForm
from ..models import MoccaRegister, MoccaRegisterContact
from .list_filters import ScreenedListFilter, ContactAttemptsListFilter, CallListFilter


class MoccaRegisterContactInline(TabularInlineMixin, admin.TabularInline):

    fields = [
        "answered",
        "respondent",
        "survival_status",
        "willing_to_attend",
        "call_again",
        "report_datetime",
    ]
    model = MoccaRegisterContact
    form = MoccaRegisterContactForm
    extra = 0


@admin.register(MoccaRegister, site=mocca_screening_admin)
class MoccaRegisterAdmin(
    TemplatesModelAdminMixin, ModelAdminFormInstructionsMixin, SimpleHistoryAdmin
):
    form = MoccaRegisterForm
    show_object_tools = True
    inlines = [MoccaRegisterContactInline]
    ordering = ["mocca_study_identifier"]

    fieldsets = (
        [None, {"fields": ("screening_identifier",)}],
        [
            "Original Enrollment Data",
            {
                "fields": (
                    "mocca_study_identifier",
                    "mocca_screening_identifier",
                    "mocca_site",
                    "first_name",
                    "last_name",
                    "initials",
                    "gender",
                    "dob",
                    "birth_year",
                    "age_in_years",
                )
            },
        ],
        ["Contact", {"fields": ("notes",)}],
        audit_fieldset_tuple,
    )

    list_display = (
        "call",
        "__str__",
        "contact_attempts",
        "date_last_called",
        "screening_identifier",
    )

    list_filter = (
        ScreenedListFilter,
        ContactAttemptsListFilter,
        CallListFilter,
        "date_last_called",
        "gender",
        "created",
        "modified",
    )

    radio_fields = {
        "gender": admin.VERTICAL,
        "mocca_site": admin.VERTICAL,
        "call": admin.VERTICAL,
    }

    search_fields = (
        "mocca_study_identifier",
        "initials",
        "mocca_screening_identifier",
        "screening_identifier",
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=None)
        fields = [
            "contact_attempts",
            "screening_identifier",
            "mocca_study_identifier",
            "mocca_screening_identifier",
            "mocca_site",
        ]
        readonly_fields = list(readonly_fields)
        for f in fields:
            if f not in readonly_fields:
                readonly_fields.append(f)
        readonly_fields = tuple(readonly_fields)
        return readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "mocca_site":
            sites = get_mocca_sites_by_country(country=get_current_country())
            kwargs["queryset"] = db_field.related_model.objects.filter(
                name__in=[v.name for v in sites.values()]
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
