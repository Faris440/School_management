from django.conf import settings
from model_utils.choices import Choices
from formset.richtext import controls


hostname = getattr(settings, "CUSTOM_HOST_NAME", None)


MIN_LENGTH = 50
MEDIUM_LENGTH = 100
LONG_LENGTH = 250
BIG_LENGTH = 400

OPTIONS_ICONS_SIZE = "16"
SIDEBAR_ICONS_SIZE = "16"
HEADER_ICONS_SIZE = "20"

TEXTAREA = {
    "rows": 4,
    "cols": 50,
    "maxlength": 5000,
    "placeholder": "une description …",
}

control_elements = [
    controls.Heading([1, 2, 3, 4, 5, 6]),
    controls.Bold(),
    controls.Italic(),
    controls.Underline(),
    controls.Separator(),
    controls.Blockquote(),
    controls.TextColor(["rgb(212, 0, 0)", "rgb(0, 212, 0)", "rgb(0, 0, 212)"]),
    controls.Separator(),
    controls.BulletList(),
    controls.OrderedList(),
    controls.Separator(),
    controls.TextIndent(),
    controls.TextIndent("outdent"),
    controls.TextMargin("increase"),
    controls.TextMargin("decrease"),
    controls.TextAlign(["left", "center", "right"]),
    controls.Separator(),
    # controls.Link(),
    controls.HorizontalRule(),
    controls.Subscript(),
    controls.Superscript(),
    controls.Separator(),
    controls.ClearFormat(),
    controls.Redo(),
    controls.Undo(),
]



