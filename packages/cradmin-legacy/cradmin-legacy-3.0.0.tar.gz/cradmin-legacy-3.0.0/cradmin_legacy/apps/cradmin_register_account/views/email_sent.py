from __future__ import unicode_literals
from django.views.generic import TemplateView


class EmailSentView(TemplateView):
    template_name = 'cradmin_register_account/email_sent.django.html'
