from django.contrib import messages
from django.utils.translation import ugettext_lazy


GRAY = 'gray'
GREEN = 'green'
BLUE = 'blue'
YELLOW = 'yellow'
RED = 'red'

NO_TITLE = ''
SUCCESS = ugettext_lazy('Éxito')
ERROR = ugettext_lazy('Error')
WARNING = ugettext_lazy('Lo sentimos')

errors_list = {
    'title': {
        '400': ugettext_lazy('Bad Request'),
        '401': ugettext_lazy('Unauthorized'),
        '403': ugettext_lazy('Prohibido'),
        '404': ugettext_lazy('Not Found'),
        '405': ugettext_lazy('Method not allowed'),
        '406': ugettext_lazy('Not Acceptable'),
        '409': ugettext_lazy('Conflicto'),
        '415': ugettext_lazy('Unsupported Media Type'),
        '500': ugettext_lazy('Error en el servidor'),
        '503': ugettext_lazy('Service Unavailable'),
        'sorry': ugettext_lazy('Lo sentimos'),
    },
    'body': {
        'no_action': ugettext_lazy(
            'We are sorry. You are trying to execute an unknown'
            ' or prohibited action.'),
        'incorrect_method': ugettext_lazy(
            'We are sorry. You are trying to execute an'
            ' action with an incorrect header or'
            ' method.'),
        'missing_step': ugettext_lazy(
            'We are sorry. You must complete the previous'
            ' steps to execute this action.'),
        'bad_login': ugettext_lazy(
            'La combinación de usuario/contraseña es inválida. Por favor'
            ' intentalo de nuevo.'),
        'no_perm': ugettext_lazy(
            'Usted no tiene suficientes permisos para ejecutar esta'
            ' acción. Si esto es un error, por favor, contacte a su'
            ' administrador.'),
        'ticket': ugettext_lazy(
            'Un error interno ha ocurrido en el sistema. El administrador ha'
            ' sido notificado.'),
        'encryption': ugettext_lazy(
            'La combinación de cer, key y contraseña es incorrecta.'
            ' Los cambios en estos 3 campos se han descartado.'),
        'verification_pending': ugettext_lazy(
            'Aún no ha verificado su correo electrónico.'),
        'verification_error': ugettext_lazy(
            'El correo no existe en el sistema o ya fue'
            ' verificado anteriormente.'),
        'email_inc_exists': ugettext_lazy(
            'El correo electrónico está en un formato'
            ' invalido o ya existe en el sistema'),
        'team_join_exists': ugettext_lazy(
            'Este usuario ya se encuentra relacionado a un negocio,'
            ' no puede crear uno nuevo con la cuenta actual.'),
        'team_plan_exists': ugettext_lazy(
            'Su negocio ya se encuentra relacionado a un plan,'
            ' no puede crear una nueva subscripción sin antes cancelar la'
            ' existente.'),
        'join_exists': ugettext_lazy(
            'Este usuario ya se encuentra relacionado a un negocio, '
            'no puede unirse a otro con la cuenta actual.'),
        'no_join_exists': ugettext_lazy(
            'Este usuario no se encuentra relacionado a ningún negocio.'),
        'no_user_exists': ugettext_lazy(
            'El usuario no existe en el sistema.'),
        'not_in_team': ugettext_lazy(
            'Usted no pertenece a este negocio.'),
        'no_team': ugettext_lazy(
            'El negocio no existe en el sistema.'),
        'team_exists': ugettext_lazy(
            'El negocio ya existe en el sistema.'),
        'already_claimed': ugettext_lazy(
            'Esta invitación ya fue procesada anteriormente.'),
        'already_in_team': ugettext_lazy(
            'El usuario ya se encuentra en este negocio.'),
        'publication_not_exists': ugettext_lazy(
            'El anuncio no existe en el sistema.'),
        'invalid_data': ugettext_lazy(
            'La información es incorrecta.'),
        'profile_not_exists': ugettext_lazy(
            'El mostrador virtual no existe en el sistema.'),
    }
}


def generate_msg(request, state=GRAY, title='Debug', body='Empty'):
    mtype = None
    if state == GRAY:
        mtype = messages.DEBUG
    elif state == GREEN:
        mtype = messages.SUCCESS
    elif state == BLUE:
        mtype = messages.INFO
    elif state == YELLOW:
        mtype = messages.WARNING
    elif state == RED:
        mtype = messages.ERROR

    messages.add_message(
        request,
        mtype,
        extra_tags=title,
        message=body,
        fail_silently=True
    )


def _parseToJSON(message):
    return {
        'level': message.level_tag,
        'tags': message.extra_tags,
        'body': message.message,
    }


def getMessagesJSON(request):
    storage = messages.get_messages(request)
    array = list()
    for message in storage:
        array.append(_parseToJSON(message))
    return array
