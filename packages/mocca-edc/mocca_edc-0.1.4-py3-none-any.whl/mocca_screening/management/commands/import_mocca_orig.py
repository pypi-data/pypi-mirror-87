import csv
import os
import sys

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from edc_constants.constants import FEMALE, MALE
from edc_sites import get_site_by_attr
from mocca_sites.sites import all_sites
from tqdm import tqdm


def import_mocca_orig(verbose=None, test=None, overwrite=None):
    model_cls = django_apps.get_model("mocca_screening.moccaregister")
    if test:
        pass  # import_for_tests(model_cls)
    else:
        path = os.path.join(os.path.expanduser(settings.ETC_DIR), "mocca_original.csv")
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(path)
        except TypeError:
            raise FileNotFoundError(f"Invalid path. Got {path}.")
        if verbose:
            sys.stdout.write(
                f"\nImporting MOCCA original patients from '{path}' "
                f"into {model_cls._meta.label_lower}\n"
            )

        if overwrite:
            model_cls.objects.all().delete()

        with open(path, "r") as f:
            file = f.readlines()
            rec_count = len(file) - 1

        import_file(path, rec_count, model_cls)

        if verbose:
            sys.stdout.write("Done.\n")


def get_field_options(row):
    new_row = {}
    if row["country"] == "1":
        country = "tanzania"
    elif row["country"] == "2":
        country = "uganda"
    else:
        raise TypeError(f"Unknown country. Got `{row['country']}`")

    if row["sex"] == "1":
        gender = MALE
    elif row["sex"] == "2":
        gender = FEMALE
    else:
        raise TypeError(f"Unknown gender. Got `{row['gender']}`")

    site = get_site_by_attr(
        "orig_site_id", int(row["site"]), sites=all_sites.get(country)
    )
    model_cls = django_apps.get_model("mocca_lists.MoccaOriginalSites")
    mocca_site_obj = model_cls.objects.get(name=site.name)

    model_cls = django_apps.get_model("sites.Site")
    site_obj = model_cls.objects.get(id=site.site_id)

    mocca_study_identifier = row["study_id"]
    if len(mocca_study_identifier) == 5:
        mocca_study_identifier = f"0{mocca_study_identifier}"

    new_row.update(
        mocca_screening_identifier=row["screening_id"],
        mocca_study_identifier=mocca_study_identifier,
        initials=row["pt_initials"],
        mocca_country=country,
        mocca_site=mocca_site_obj,
        gender=gender,
        age_in_years=row["age"],
        birth_year=row["birth_year"],
        dob=row["dob"],
        site=site_obj,
    )
    return new_row


def import_file(path, rec_count, model_cls):
    fieldnames = [
        "country",
        "site",
        "screening_id",
        "study_id",
        "pt_initials",
        "dob",
        "birth_year",
        "age",
        "sex",
    ]

    with open(path, "r") as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for index, row in tqdm(enumerate(reader), total=rec_count):
            if index == 0:
                continue
            opts = get_field_options(row)
            try:
                obj = model_cls.objects.get(
                    mocca_study_identifier=opts.get("mocca_study_identifier")
                )
            except ObjectDoesNotExist:
                model_cls.objects.create(**opts)
            else:
                for k, v in opts.items():
                    if k != "mocca_study_identifier":
                        setattr(obj, k, v)
                obj.save()


class Command(BaseCommand):

    help = "Import country holidays"

    def handle(self, *args, **options):
        try:
            import_mocca_orig(verbose=True)
        except FileNotFoundError as e:
            raise CommandError(f"File not found. Got {e}")
