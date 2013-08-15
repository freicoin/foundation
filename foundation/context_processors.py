from django.conf import settings # import the settings file

def settings_to_templates(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'FRC_EXPLORER': settings.FRC_EXPLORER,
            'BTC_EXPLORER': settings.BTC_EXPLORER
            }
