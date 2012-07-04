from django.db import models
from django.utils.translation import ugettext_lazy as _
from privatebeta.views import accept
import datetime

class InviteRequest(models.Model):
    email = models.EmailField(_('Email address'), unique=True)
    created = models.DateTimeField(_('Created'), auto_now=True)
    invited = models.BooleanField(_('Invited'), default=False)

    def __unicode__(self):
        return _('Invite for %(email)s') % {'email': self.email}
    def accept(self):
        accept(self.email)