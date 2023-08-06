from edc_visit_schedule import FormsCollection, Crf

crfs_prn = FormsCollection(
    # Crf(show_order=175, model="mocca_subject.healtheconomicsrevised"),
    Crf(show_order=178, model="mocca_subject.familyhistory"),
    Crf(show_order=180, model="mocca_subject.nextappointment"),
    Crf(show_order=200, model="mocca_subject.cd4result"),
    Crf(show_order=210, model="mocca_subject.glucose"),
    Crf(show_order=220, model="mocca_subject.viralloadresult"),
    name="prn",
)

crfs_unscheduled = FormsCollection(
    Crf(show_order=110, model="mocca_subject.clinicalreview"),
    Crf(show_order=111, model="mocca_subject.indicators"),
    Crf(show_order=112, model="mocca_subject.hivinitialreview", required=False),
    Crf(show_order=114, model="mocca_subject.dminitialreview", required=False),
    Crf(show_order=116, model="mocca_subject.htninitialreview", required=False),
    Crf(show_order=120, model="mocca_subject.hivreview", required=False),
    Crf(show_order=130, model="mocca_subject.dmreview", required=False),
    Crf(show_order=140, model="mocca_subject.htnreview", required=False),
    Crf(show_order=145, model="mocca_subject.medications"),
    Crf(show_order=150, model="mocca_subject.drugrefillhtn", required=False),
    Crf(show_order=160, model="mocca_subject.drugrefilldm", required=False),
    Crf(show_order=170, model="mocca_subject.drugrefillhiv", required=False),
    Crf(show_order=185, model="mocca_subject.hivmedicationadherence", required=False),
    Crf(show_order=190, model="mocca_subject.dmmedicationadherence", required=False),
    Crf(show_order=195, model="mocca_subject.htnmedicationadherence", required=False),
    Crf(show_order=200, model="mocca_subject.complicationsfollowup", required=False),
    Crf(show_order=220, model="mocca_subject.familyhistory"),
    Crf(show_order=230, model="mocca_subject.nextappointment"),
    name="unscheduled",
)

crfs_missed = FormsCollection(
    Crf(show_order=10, model="mocca_subject.subjectvisitmissed"), name="missed",
)


crfs_d1 = FormsCollection(
    Crf(show_order=100, model="mocca_subject.clinicalreviewbaseline"),
    Crf(show_order=110, model="mocca_subject.indicators"),
    Crf(show_order=120, model="mocca_subject.hivinitialreview", required=False),
    Crf(show_order=130, model="mocca_subject.dminitialreview", required=False),
    Crf(show_order=140, model="mocca_subject.htninitialreview", required=False),
    Crf(show_order=143, model="mocca_subject.medications"),
    Crf(show_order=145, model="mocca_subject.drugrefillhtn", required=False),
    Crf(show_order=150, model="mocca_subject.drugrefilldm", required=False),
    Crf(show_order=155, model="mocca_subject.drugrefillhiv", required=False),
    Crf(show_order=160, model="mocca_subject.otherbaselinedata"),
    Crf(show_order=165, model="mocca_subject.complicationsbaseline"),
    Crf(show_order=170, model="mocca_subject.nextappointment"),
    name="day1",
)
crfs_6m = FormsCollection(
    Crf(show_order=110, model="mocca_subject.clinicalreview"),
    Crf(show_order=115, model="mocca_subject.indicators"),
    Crf(show_order=112, model="mocca_subject.hivinitialreview", required=False),
    Crf(show_order=114, model="mocca_subject.dminitialreview", required=False),
    Crf(show_order=116, model="mocca_subject.htninitialreview", required=False),
    Crf(show_order=130, model="mocca_subject.hivreview", required=False),
    Crf(show_order=140, model="mocca_subject.dmreview", required=False),
    Crf(show_order=150, model="mocca_subject.htnreview", required=False),
    Crf(show_order=155, model="mocca_subject.medications"),
    Crf(show_order=160, model="mocca_subject.drugrefillhtn", required=False),
    Crf(show_order=170, model="mocca_subject.drugrefilldm", required=False),
    Crf(show_order=180, model="mocca_subject.drugrefillhiv", required=False),
    Crf(show_order=185, model="mocca_subject.hivmedicationadherence", required=False),
    Crf(show_order=190, model="mocca_subject.dmmedicationadherence", required=False),
    Crf(show_order=195, model="mocca_subject.htnmedicationadherence", required=False),
    Crf(show_order=200, model="mocca_subject.complicationsfollowup", required=False),
    Crf(show_order=210, model="mocca_subject.healtheconomicsrevised"),
    Crf(show_order=220, model="mocca_subject.familyhistory"),
    Crf(show_order=230, model="mocca_subject.nextappointment"),
    name="6m",
)

crfs_12m = FormsCollection(
    Crf(show_order=110, model="mocca_subject.clinicalreview"),
    Crf(show_order=115, model="mocca_subject.indicators"),
    Crf(show_order=112, model="mocca_subject.hivinitialreview", required=False),
    Crf(show_order=114, model="mocca_subject.dminitialreview", required=False),
    Crf(show_order=116, model="mocca_subject.htninitialreview", required=False),
    Crf(show_order=120, model="mocca_subject.hivreview", required=False),
    Crf(show_order=130, model="mocca_subject.dmreview", required=False),
    Crf(show_order=140, model="mocca_subject.htnreview", required=False),
    Crf(show_order=145, model="mocca_subject.medications"),
    Crf(show_order=150, model="mocca_subject.drugrefillhtn", required=False),
    Crf(show_order=160, model="mocca_subject.drugrefilldm", required=False),
    Crf(show_order=170, model="mocca_subject.drugrefillhiv", required=False),
    Crf(show_order=185, model="mocca_subject.hivmedicationadherence", required=False),
    Crf(show_order=190, model="mocca_subject.dmmedicationadherence", required=False),
    Crf(show_order=195, model="mocca_subject.htnmedicationadherence", required=False),
    Crf(show_order=200, model="mocca_subject.complicationsfollowup", required=False),
    Crf(show_order=210, model="mocca_subject.healtheconomicsrevised", required=False),
    Crf(show_order=220, model="mocca_subject.familyhistory"),
    name="12m",
)
