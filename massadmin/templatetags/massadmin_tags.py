# -*- coding: utf-8 -*-

from django import template

from massadmin.forms import MassOptionsForField

register = template.Library()

@register.inclusion_tag('massadmin/mass_options_form.html', takes_context=True)
def render_mass_options_for_field(context, field_name, field=None):
    """
    Render mass options form for a given model's field or inline.

    If `field` is not given, it means `field_name` identifies an inline.
    """
    request = context['request']

    form = MassOptionsForField(field_name=field_name, field=field)

    return {
        'form': form
    }