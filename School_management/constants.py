from django.conf import settings
from model_utils.choices import Choices


hostname = getattr(settings, "CUSTOM_HOST_NAME", None)


MIN_LENGTH = 50
MEDIUM_LENGTH = 100
LONG_LENGTH = 250
BIG_LENGTH = 400

OPTIONS_ICONS_SIZE = "16"
SIDEBAR_ICONS_SIZE = "16"
HEADER_ICONS_SIZE = "20"



