import os
import pdb
import sys
import csv

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import color_style
from edc_constants.constants import FEMALE, MALE
from edc_facility.import_holidays import import_file
from mocca_lists.models import MoccaOriginalSites
from tqdm import tqdm


style = color_style()


class ImportMoccaError(Exception):
    pass


def import_mocca_register(verbose=None):
    model_cls = django_apps.get_model("mocca_screening.moccaregister")
    fieldnames = [
        "country",
        "site",
        "screening_id",
        "study_id",
        "initials",
        "birth_year",
        "age_in_years",
        "gender",
    ]
    path = settings.MOCCA_REGISTER_FILE
    try:
        if not os.path.exists(path):
            raise ImportMoccaError(path)
    except TypeError:
        raise ImportMoccaError(f"Invalid path. Got {path}.")
    if verbose:
        sys.stdout.write(
            f"\nImporting MOCCA register from '{path}' "
            f"into {model_cls._meta.label_lower}\n"
        )
    model_cls.objects.all().delete()

    with open(path, "r") as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        rows = [row for row in reader]

    import_file(path, model_cls, fieldnames)

    if verbose:
        sys.stdout.write("Done.\n")


def import_file(path, model_cls, fieldnames):
    sys.stdout.write(style.MIGRATE_HEADING("\n Importing mocca register.\n"))
    with open(path, "r") as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        total = len([row for row in reader])
    with open(path, "r") as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for index, row in tqdm(enumerate(reader), total=total):
            if index == 0:
                continue
            try:
                model_cls.objects.get(mocca_study_identifier=row["study_id"])
            except ObjectDoesNotExist:
                mocca_site = MoccaOriginalSites.objects.get(name=row["site"].lower())
                model_cls.objects.create(
                    mocca_country=row["country"].lower(),
                    mocca_site=mocca_site,
                    mocca_screening_identifier=row["screening_id"],
                    mocca_study_identifier=row["study_id"],
                    initials=(row["initials"] or "").upper(),
                    birth_year=row["birth_year"],
                    age_in_years=row["age_in_years"],
                    gender=MALE if row["gender"] == "MALE" else FEMALE,
                )
