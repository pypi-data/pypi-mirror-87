import os

from html2text import html2text
from smtplib import SMTPException

from django.core.mail import EmailMultiAlternatives
from django.template import loader


default_app_config = 'fs_email.apps.FsEmailConfig'


def send_email(addr_from, addr_to, subject, template, context, attachments=None, reply_to=None):
    from .models import Email

    # Allow for a single address to be passed in.
    if isinstance(addr_to, str):
        addr_to = [addr_to]

    body_html = loader.get_template(template).render(context)
    alternatives_parts = [(body_html, 'text/html')]

    body_txt = html2text(body_html)

    # Load attachments and create name/data tuples.
    attachments_parts = []
    for attachment in attachments or []:
        # Attachments can be pairs of name/data, or filesystem paths.
        if not hasattr(attachment, '__iter__'):
            with open(attachment, 'rb') as f:
                attachments_parts.append((os.path.basename(attachment), f.read()))
        else:
            attachments_parts.append(attachment)

    headers = reply_to and {'Reply-To': reply_to}

    msg = EmailMultiAlternatives(subject=subject, body=body_txt, from_email=addr_from, to=addr_to, alternatives=alternatives_parts, attachments=attachments_parts, headers=headers)

    try:
        msg.send()
    except SMTPException as ex:
        status = str(ex)
    else:
        status = 'OK'

    Email.objects.create(whom=', '.join(addr_to), subject=subject, body=body_html, status=status)
