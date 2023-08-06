from edc_action_item.site_action_items import site_action_items
from edc_ltfu.action_items import LossToFollowupAction as BaseLossToFollowupAction
from edc_offstudy.action_items import EndOfStudyAction as BaseEndOfStudyAction
from edc_prn.action_items import (
    ProtocolDeviationViolationAction as BaseProtocolDeviationViolationAction,
    UnblindingRequestAction as BaseUnblindingRequestAction,
    UnblindingReviewAction as BaseUnblindingReviewAction,
)


class EndOfStudyAction(BaseEndOfStudyAction):

    reference_model = "mocca_prn.endofstudy"
    admin_site_name = "mocca_prn_admin"


class LossToFollowupAction(BaseLossToFollowupAction):

    reference_model = "mocca_prn.losstofollowup"
    admin_site_name = "mocca_prn_admin"


class ProtocolDeviationViolationAction(BaseProtocolDeviationViolationAction):
    reference_model = "mocca_prn.protocoldeviationviolation"
    admin_site_name = "mocca_prn_admin"


class UnblindingRequestAction(BaseUnblindingRequestAction):
    reference_model = "mocca_prn.unblindingrequest"
    admin_site_name = "mocca_prn_admin"


class UnblindingReviewAction(BaseUnblindingReviewAction):
    reference_model = "mocca_prn.unblindingreview"
    admin_site_name = "mocca_prn_admin"


site_action_items.register(EndOfStudyAction)
site_action_items.register(LossToFollowupAction)
site_action_items.register(ProtocolDeviationViolationAction)
site_action_items.register(UnblindingRequestAction)
site_action_items.register(UnblindingReviewAction)
