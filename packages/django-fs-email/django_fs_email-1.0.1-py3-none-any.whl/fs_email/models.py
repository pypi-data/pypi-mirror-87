from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _


class Email(models.Model):
    when = models.DateTimeField(verbose_name=_('when'), auto_now_add=True)
    whom = models.CharField(verbose_name=_('whom'), max_length=255)
    subject = models.CharField(verbose_name=_('subject'), max_length=255)
    body = models.TextField(verbose_name=_('body'))
    status = models.CharField(verbose_name=_('status'), max_length=255)

    class Meta:
        verbose_name = _('email')
        verbose_name_plural = _('emails')

    def __unicode__(self):
        return ugettext('Email #{0}').format(self.id)
