# Obtained and modified from:
# http://goo.gl/XDH8QX

from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm as PRF
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.urls import reverse
from django.utils.encoding import force_bytes
from celery.utils.log import get_task_logger
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext

from Wuafbox.tasks import sendMail

logger = get_task_logger('MainAPP.tasks')


class PasswordResetForm(PRF):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = ugettext(
            "alguien123@gmail.com")
        self.fields['email'].label = ugettext(
            "Correo Electrónico de la cuenta")

    def send_mail(self, email_template_id,
                  context, from_email, to_email,
                  html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        substitutions = {
            'to': to_email,
            'substitutions': {
                'subject': 'Recuperar mi contraseña de Wuafbox',
                'cta_text': 'Recuperar contraseña',
                'body': '''
                        <p>Para confirmar tu correo electrónico y recuperar tu contraseña da clic en el siguiente link:</p>
                    ''',
            },
            'html_content': '<strong>Recuperar contraseña</strong>',
            'template_id': email_template_id,
        }
        substitutions['substitutions'].update(context)
        sendMail(substitutions)


    def save(self, email_template_id, domain_override=None,
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override

            # {'-name-': self.validated_data['name'],
            #  '-company-': self.validated_data['company'],
            #  '-email-': self.validated_data['email'],
            #  '-accounts-': self.validated_data['accounts'],
            #  '-message-': self.validated_data['message']},
            protocol = 'https' if use_https else 'http'
            context = {
                'first_name': user.first_name,
                'cta_link': protocol + '://' + domain + reverse(
                    'password_reset_confirm', kwargs={
                        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
                        'token': token_generator.make_token(user),
                    })}
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(
                email_template_id=email_template_id,
                context=context,
                from_email=from_email,
                to_email=(user.email, user.first_name),
                html_email_template_name=html_email_template_name
            )

