# -*- coding: utf-8 -*-

from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

from extended_choices import Choices

CHARFIELD_ACTIONS = Choices(
    ('DEFINE', 'define', _('Define (if empty)')),
    ('REPLACE', 'replace', _('Replace')),
    ('PREPEND', 'prepend', _('Add before')),
    ('APPEND', 'append', _('Add after'))
)


class MassOptionsForField(forms.Form):
    """
    A dynamic form that displays mass change options for a given model field
    (or model inline).

    In most case, it just generates a checkbox to allow user
    to choose whether or not he wants to handle mass change of this given
    field/inline.
    If given field is a CharField and its widget is not
    a sub-instance of MultiWidget, expose more advanced options like
    'prepend', 'append', 'empty', etc.

    Note: it also works for inlines. In that case, only `field_name` is given
    in the extra kwargs.
    """
    CHARFIELD_ACTIONS = CHARFIELD_ACTIONS
    def __init__(self, *args, **kwargs):
        self.model_field_name = kwargs.pop('field_name')
        self.model_field = kwargs.pop('field', None)
        super(MassOptionsForField, self).__init__(*args, **kwargs)

        mass_field_name = self.get_mass_field_name()

        # Always create an "activate mass change" checkbox
        self.fields[mass_field_name] = forms.BooleanField(required=False)

        if self.model_field is not None:
            # If a real field has been given (i.e. not an inline), optionally
            # add mass change options (prepend, append, etc.) if
            # to field type and field widget allow it
            if isinstance(self.model_field, forms.CharField) and not isinstance(self.model_field.widget, widgets.MultiWidget):
                # If field is a CharField subclass and its widget is not a
                # MultiWidget subclass, we can assume there will be *only one*
                # key for this field in POST data. We will then be able to
                # alter it dynamically (as a raw string) *before*
                # submitting it to ModelForm.
                self.fields[mass_field_name + '_action'] = forms.ChoiceField(choices=CHARFIELD_ACTIONS)

    def get_mass_field_name(self):
        return '_mass_change_' + self.model_field_name