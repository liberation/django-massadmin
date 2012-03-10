# -*- coding: utf-8 -*-

from django import template

from massadmin.forms import MassOptionsForField

register = template.Library()

@register.inclusion_tag('massadmin/mass_options_form.html', takes_context=True)
def render_mass_options_for_field(context, field, field_name):
    """
    Render mass options form for a given model's field.
    """
    request = context['request']

    form = MassOptionsForField(field=field, field_name=field_name)

    return {
        'form': form
    }
        
    
