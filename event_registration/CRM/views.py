from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'CRM/signup.html'


class CustomPermissionDeniedView(TemplateView):
    template_name = '403.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return HttpResponseForbidden(response.render())