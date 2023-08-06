from django.conf import settings


DISCOUNT_DEFAULT_DURATION = getattr(settings, 'DISCOUNT_DEFAULT_DURATION', 30)      # Days

