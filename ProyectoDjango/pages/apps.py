from django.apps import AppConfig


class PagesConfig(AppConfig):
    defeault_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    verbose_name = "Gestion de paginas"
