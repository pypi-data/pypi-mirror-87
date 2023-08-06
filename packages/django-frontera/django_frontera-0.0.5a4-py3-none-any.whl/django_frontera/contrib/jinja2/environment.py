from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.utils.translation import gettext, ngettext

from jinja2 import Environment

# DEPRECATED .... NOT REQUIRED. USED DJANGO_JINJA INSTEAD OF PLAIN JINJA2


# def environment(**options):
#     env = Environment(**options)
#     env.globals.update({
#        'static': staticfiles_storage.url,
#        'url': reverse,
#     })
#     return env


def environment(**options):
    options['extensions'] += ['jinja2.ext.i18n']
    env = Environment(**options)

    env.install_gettext_callables(
        gettext=gettext, ngettext=ngettext, newstyle=True)

    env.globals.update({
        'get_messages': messages.get_messages,
    })
    return env
