from django.conf import settings


def supporto_telefonico(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'SUPPORTO_TELEFONICO': getattr(settings, 'SUPPORTO_TELEFONICO', False)}


def show_git_info(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'GIT_INFO': getattr(settings, 'GIT_INFO', True)}
