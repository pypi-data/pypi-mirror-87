from edc_visit_schedule import FormsCollection, Requisition
from mocca_labs import (
    blood_glucose_panel,
    blood_glucose_poc_panel,
    hba1c_panel,
    hba1c_poc_panel,
)

requisitions_prn = FormsCollection(
    Requisition(
        show_order=10, panel=blood_glucose_panel, required=True, additional=False
    ),
    Requisition(
        show_order=20, panel=blood_glucose_poc_panel, required=True, additional=False
    ),
    Requisition(show_order=30, panel=hba1c_poc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=hba1c_panel, required=True, additional=False),
    name="requisitions_prn",
)

requisitions_d1 = FormsCollection(name="requisitions_day1",)
requisitions_6m = FormsCollection(name="requisitions_6m",)
requisitions_12m = FormsCollection(name="requisitions_month12",)
