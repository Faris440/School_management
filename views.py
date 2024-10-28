from django.shortcuts import render
from django.urls import reverse
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name="index.html"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        return context
class RedirectionView(RedirectView):
    # URL par défaut si l'utilisateur n'est pas authentifié
    url = "/home/"

        
    