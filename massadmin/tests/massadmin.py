# -*- coding: utf-8 -*-

from .boats.models import Boat
from .base import BaseTest


class CharFieldTest(BaseTest):

    def test_define_only_if_empty(self):
        b1 = self.F.Boat()
        b2 = self.F.Boat(architect="Bruce Farr")  # Should not be modified
        b3 = self.F.Boat()
        b4 = self.F.Boat()  # Will not be edited
        form = self.get_massadmin_form(b1, b2, b3)
        architect = u"William Fife"
        self.update_form(form, architect=architect)
        form.submit().follow()
        self.assertEqual(Boat.objects.get(pk=b1.pk).architect, architect)
        self.assertNotEqual(Boat.objects.get(pk=b2.pk).architect, architect)
        self.assertEqual(Boat.objects.get(pk=b3.pk).architect, architect)
        self.assertNotEqual(Boat.objects.get(pk=b4.pk).architect, architect)

    def test_replace(self):
        b1 = self.F.Boat()
        b2 = self.F.Boat(architect="Bruce Farr")
        b3 = self.F.Boat()  # Will not be edited
        form = self.get_massadmin_form(b1, b2)
        architect = u"William Fife"
        self.update_form(form, architect=architect, architect_action="replace")
        form.submit().follow()
        self.assertEqual(Boat.objects.get(pk=b1.pk).architect, architect)
        self.assertEqual(Boat.objects.get(pk=b2.pk).architect, architect)
        self.assertNotEqual(Boat.objects.get(pk=b3.pk).architect, architect)

    def test_prepend(self):
        b1 = self.F.Boat(name="Duick I")
        b2 = self.F.Boat(name="Duick II")
        b3 = self.F.Boat(name="Pen Duick III")  # Will not be edited
        form = self.get_massadmin_form(b1, b2)
        self.update_form(form, name="Pen ", name_action="prepend")
        form.submit().follow()
        self.assertEqual(Boat.objects.get(pk=b1.pk).name, "Pen Duick I")
        self.assertEqual(Boat.objects.get(pk=b2.pk).name, "Pen Duick II")
        self.assertEqual(Boat.objects.get(pk=b3.pk).name, "Pen Duick III")

    def test_append(self):
        b1 = self.F.Boat(name="Pen")
        b2 = self.F.Boat(name="Pen")
        b3 = self.F.Boat(name="Pen Duick")  # Will not be edited
        form = self.get_massadmin_form(b1, b2)
        self.update_form(form, name=" Duick", name_action="append")
        form.submit().follow()
        self.assertEqual(Boat.objects.get(pk=b1.pk).name, "Pen Duick")
        self.assertEqual(Boat.objects.get(pk=b2.pk).name, "Pen Duick")
        self.assertEqual(Boat.objects.get(pk=b3.pk).name, "Pen Duick")
