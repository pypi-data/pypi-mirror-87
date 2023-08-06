import uuid
from django.contrib.auth import get_user_model
from django.db import models
from djangoldp.models import Model

from django.utils.translation import ugettext_lazy as _

class Contact(Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="contacts", null=True, blank=True)
    contact = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.urlid)

    class Meta(Model.Meta):
        verbose_name = _('contact')
        verbose_name_plural = _("contacts")
        auto_author = 'user'
        owner_field = 'user'
        anonymous_perms = []
        authenticated_perms = []
        owner_perms = ['view', 'delete']
        rdf_type = "sib:contact"
