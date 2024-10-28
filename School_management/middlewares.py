from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect

PUBLIC_NAMED_URLS = getattr(settings, "PUBLIC_NAMED_URLS", ())

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Récupérer le nom de l'URL
        url_name = resolve(request.path_info).url_name

        # Vérifier si l'utilisateur est authentifié ou l'URL est publique
        if request.user.is_authenticated or url_name in PUBLIC_NAMED_URLS:
            return None  # Autoriser l'accès

        # Redirection vers la page de login si non authentifié
        return redirect(settings.LOGIN_URL)
