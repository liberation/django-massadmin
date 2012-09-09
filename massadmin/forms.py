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

MULTI_ACTIONS = Choices(
    ('DEFINE', 'define', _('Define (if empty)')),
    ('REPLACE', 'replace', _('Replace')),
    ('ADD', 'add', _('Add')),
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
    MULTI_ACTIONS = MULTI_ACTIONS

    def __init__(self, *args, **kwargs):
        self.model_field_name = kwargs.pop('field_name')
        self.model_field = kwargs.pop('field', None)
        super(MassOptionsForField, self).__init__(*args, **kwargs)

        mass_field_name = self.get_mass_field_name()

        # Always create an "activate mass change" checkbox
        self.fields[mass_field_name] = forms.BooleanField(required=False, label=_('Mass change'))

        self.create_actions_field()

    def create_actions_field(self):
        """
        If a real field has been given (i.e. not an inline), optionally
        add mass change options (prepend, append, etc.) according
        to field type and field widget
        """
        if self.model_field is not None:
            mass_field_name = self.get_mass_field_name()
            if isinstance(self.model_field, forms.CharField) and not isinstance(self.model_field.widget, widgets.MultiWidget):
                # If field is a CharField subclass and its widget is not a
                # MultiWidget subclass, we can assume there will be *only one*
                # key for this field in POST data. We will then be able to
                # alter it dynamically (as a raw string) *before*
                # submitting it to ModelForm.
                choices = self.CHARFIELD_ACTIONS
            elif isinstance(self.model_field, forms.ModelMultipleChoiceField):
                choices = self.MULTI_ACTIONS
            else:
                choices = None
            if choices:
                self.fields[mass_field_name + '_action'] = forms.ChoiceField(choices=choices, label=_('Advanced operations'))

    def get_mass_field_name(self):
        return '_mass_change_' + self.model_field_name
