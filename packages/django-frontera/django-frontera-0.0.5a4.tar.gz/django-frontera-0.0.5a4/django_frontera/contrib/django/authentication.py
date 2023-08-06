# Obtained and modified from:
# http://goo.gl/aeWc10

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import ugettext as _ug
from django.views.decorators.csrf import csrf_protect

from . import messages as msgs
from .authenticationForms import PasswordResetForm


# Create your views here.
def LoginView(request):
    if request.user.is_authenticated():
        return redirect(request.get_host())

    else:
        email = password = ''
        next = request.GET.get('next', '')

        if request.method == 'POST':
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            remember = request.POST.get('remember', None)
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if remember is not None:
                        request.session.set_expiry(72000)
                    else:
                        request.session.set_expiry(0)
                    msgs.generate_msg(
                        request, msgs.GREEN, " ",
                        _ug("Bienvenido de regreso!"))

                    if next == '' or next is None:
                        return redirect(request.get_host())
                    else:
                        return redirect(next)
                else:
                    msgs.generate_msg(
                        request,
                        msgs.ERROR,
                        msgs.errors_list['title']['400'],
                        msgs.errors_list['body']['bad_login']
                    )
            else:
                msgs.generate_msg(request, msgs.RED,
                                  msgs.errors_list['title']['400'],
                                  msgs.errors_list['body']['bad_login'])

        return render_to_response(
            'login.jinja',
            {'next': next, },
            context_instance=RequestContext(request),
        )


def LogoutView(request):
    logout(request)
    return redirect('%s' % (settings.LOGIN_URL))


@csrf_protect
def password_reset(request,
                   email_template_id,
                   template_name='registration/password_reset_form.html',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   extra_context=None,
                   html_email_template_name=None,
                   extra_email_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_id': email_template_id,
                'request': request,
                'html_email_template_name': html_email_template_name,
                'extra_email_context': extra_email_context,
            }
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _ug('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
