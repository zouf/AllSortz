from django.core.mail.message import EmailMessage
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
import logging


logger = logging.getLogger(__name__)
class InviteRequest(models.Model):
    email = models.EmailField(_('Email address'), unique=True)
    created = models.DateTimeField(_('Created'), auto_now=True)
    invited = models.BooleanField(_('Invited'), default=False)

    def __unicode__(self):
        return _('Invite for %(email)s') % {'email': self.email}
    
    def save(self, *args, **kwargs):
        super(InviteRequest, self).save(*args, **kwargs)
        if self.invited:
            self.accept()
    
    def accept(self):
        try:
            mail = EmailMessage('Welcome to AllSortz!', 'Go to http://www.allsortz.com/accounts/register/ to register your account\n\n-The AllSortz Team ', to=[self.email])
            mail.send()
        except:
            logger.error('Invalid invite request')
            print('error invalid invite request')
