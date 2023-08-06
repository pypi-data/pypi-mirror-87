from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ConfigurationConfig(AppConfig):
    name = 'django_frontera.configuration'
    label = 'configuration'
    verbose_name = _('Configuration')
