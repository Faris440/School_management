from django.http import HttpRequest
from django.urls import resolve

from School_management.constants import (
    SIDEBAR_ICONS_SIZE,
    OPTIONS_ICONS_SIZE,
    HEADER_ICONS_SIZE,
)


def get_icons_size(request: HttpRequest):
    return {
        "sidebar_size": SIDEBAR_ICONS_SIZE,
        "option_size": OPTIONS_ICONS_SIZE,
        "header_size": HEADER_ICONS_SIZE,
    }