from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = "mocca_auth"
    verbose_name = "MOCCA Authentication and Permissions"
