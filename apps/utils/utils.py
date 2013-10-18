from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context

from django.contrib.sites.models import Site

def send_html_mail(template, context, subject, from_mail, to_mails):
    
    context.update({'SITE_NAME': Site.objects.get_current().name})
    context.update({'SITE_URL': "http://%s" % Site.objects.get_current().domain})
    mail_template = get_template(template)
    mail_content = mail_template.render(Context(context))
    msg = EmailMessage(subject, mail_content, from_mail, to_mails.split(','))
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
