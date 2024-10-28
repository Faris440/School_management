from django.views.generic import *


class IndexTemplateView( TemplateView):
    template_name="index.html"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        return context
class RedirectionView(RedirectView):
    url = "/home/"

        
    