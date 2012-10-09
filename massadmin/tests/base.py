# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.management import call_command
from django.db.models import loading
from django.contrib.auth.models import User

from django_webtest import WebTest

from .boats.models import Factory, Boat


class BaseTest(WebTest):

    F = Factory()
    apps = ("massadmin.tests.boats",)

    def get_massadmin_form(self, *instances):
        """
        insts are Boat instances to mass edit.
        """
        info = Boat._meta.app_label, Boat._meta.module_name
        selected = ','.join(str(i.pk) for i in instances)
        massadmin_url = reverse('admin:%s_%s_massadmin' % info, args=(selected,), )
        response = self.app.get(massadmin_url, user=self.user)
        return response.forms['boat_form']

    def update_form(self, form, **kwargs):
        """
        Just pass fields to change as kwargs.
        If you want a special action (replace, define, append, ...)
        pass yourfieldname_action kwargs with the right value.
        """
        for field_name, field_value in kwargs.iteritems():
            if field_name.endswith("_action"):
                # it's not a field, but the action requested for this field
                continue
            form[field_name] = field_value
            # We want this field to be considered
            form['_mass_change_%s' % field_name].checked = True
            action = "%s_action" % field_name
            if action in kwargs:
                # A non default action is requested
                form['_mass_change_%s_action' % field_name] = kwargs[action]

    def update_inlines(self, form, **kwargs):
        """
        Each kwarg must have this structure:
        fieldname: [
            {
                inline_field_name_a: inline_field_value,
                inline_field_name_b: inline_field_value,
            },
            ... (one dict by inline to create)
        ]
        """
        for field_name, inline_kargs_set in kwargs.iteritems():
            form['_mass_change_%s_set' % field_name].checked = True
            for idx, inline_kargs in enumerate(inline_kargs_set):
                for inline_field_name, inline_field_value in inline_kargs.iteritems():
                    form['%s_set-%s-%s' % (field_name, idx, inline_field_name)] = inline_field_value

    def _pre_setup(self):
        """
        Needed to make the tests models available.
        From http://stackoverflow.com/a/2672444.
        """
        # Add the models to the db.
        self._original_installed_apps = list(settings.INSTALLED_APPS)
        for app in self.apps:
            settings.INSTALLED_APPS.append(app)
        loading.cache.loaded = False
        call_command('syncdb', interactive=False, verbosity=0)
        # Call the original method that does the fixtures etc.
        super(BaseTest, self)._pre_setup()

    def _post_teardown(self):
        # Call the original method.
        super(BaseTest, self)._post_teardown()
        # Restore the settings.
        settings.INSTALLED_APPS = self._original_installed_apps
        loading.cache.loaded = False

    def setUp(self):
        self.user = User.objects.create_user(
            "testuser",
            "testuser@test.com",
            "testpass",
        )
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
