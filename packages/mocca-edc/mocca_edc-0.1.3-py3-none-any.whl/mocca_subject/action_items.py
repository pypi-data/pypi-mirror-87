from django.core.exceptions import ImproperlyConfigured
from edc_action_item.site_action_items import site_action_items
from edc_ltfu.constants import LOSS_TO_FOLLOWUP_ACTION
from edc_visit_tracking.action_items import VisitMissedAction
from mocca_visit_schedule.constants import SCHEDULE


class SubjectVisitMissedAction(VisitMissedAction):
    reference_model = "mocca_subject.subjectvisitmissed"
    admin_site_name = "mocca_subject_admin"
    loss_to_followup_action_name = None

    def get_loss_to_followup_action_name(self):
        schedule = self.reference_obj.visit.appointment.schedule
        if schedule.name == SCHEDULE:
            return LOSS_TO_FOLLOWUP_ACTION
        raise ImproperlyConfigured(
            "Unable to determine action name. Schedule name not known. "
            f"Got {schedule.name}."
        )


site_action_items.register(SubjectVisitMissedAction)
