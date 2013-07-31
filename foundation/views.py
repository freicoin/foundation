from django.views.generic import TemplateView

home = TemplateView.as_view(template_name='index.html')
about = TemplateView.as_view(template_name='about.html')

