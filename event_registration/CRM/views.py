from django.http import HttpResponseForbidden
from django.views.generic import TemplateView


class CustomPermissionDeniedView(TemplateView):
    template_name = '403.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return HttpResponseForbidden(response.render())
