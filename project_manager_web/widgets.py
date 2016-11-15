from django.forms import Widget
from django.forms.utils import flatatt
from django.utils import formats
from django.utils.encoding import force_text
from django.utils.html import format_html


class CustomDatePickerInput(Widget):
    """
    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    """
    def format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))
        return format_html('<date-picker{} />', flatatt(final_attrs))
