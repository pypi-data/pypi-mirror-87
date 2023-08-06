from django.conf import settings

def templates_variables(request):
    context = dict()
    if hasattr(settings,"TEMPLATES_VARIABLES"):
        context.update(settings.TEMPLATES_VARIABLES)
    return context

