from django.conf import settings

def settings_to_templates(request=None):
    # return values from the settings as a dictionnary.
    return {'FRC_EXPLORER': settings.FRC_EXPLORER,
            'BTC_EXPLORER': settings.BTC_EXPLORER
            }
