# -*- coding: utf-8 -*-

from .boats.models import Boat
from .base import BaseTest


class GenericTest(BaseTest):

    def test_that_nothing_is_modified_if_nothing_checked(self):
        b1 = self.F.Boat(name="Pen Duick", rigging=Boat.KETCH)
        form = self.get_massadmin_form(b1)
        form.submit().follow()
        self.assertEqual(Boat.objects.get(pk=b1.pk).name, b1.name)
        self.assertEqual(Boat.objects.get(pk=b1.pk).rigging, b1.rigging)


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


class ChoicesFieldTest(BaseTest):

    def test_no_action_available(self):
        # append, prepend, etc. makes no sense for a choice field
        b1 = self.F.Boat(name="Pen Duick")
        b2 = self.F.Boat(name="Pen Duick II")
        form = self.get_massadmin_form(b1, b2)
        self.assertTrue("_mass_change_rigging_action" not in form.fields)

    def test_replace_select(self):
        b1 = self.F.Boat()
        b2 = self.F.Boat(rigging=Boat.CUTTER)
        b3 = self.F.Boat()  # Will not be edited
        # test Boats previous values
        self.assertEqual(Boat.objects.get(pk=b1.pk).rigging, Boat.SLOOP)
        self.assertEqual(Boat.objects.get(pk=b2.pk).rigging, Boat.CUTTER)
        form = self.get_massadmin_form(b1, b2)
        self.update_form(form, rigging=Boat.KETCH)
        form.submit().follow()
        self.assertEqual(Boat.objects.get(pk=b1.pk).rigging, Boat.KETCH)
        self.assertEqual(Boat.objects.get(pk=b2.pk).rigging, Boat.KETCH)
        self.assertEqual(Boat.objects.get(pk=b3.pk).rigging, Boat.SLOOP)


class FloatFieldTest(BaseTest):

    def test_no_action_available(self):
        # append, prepend, etc., makes no sense for a float field
        b1 = self.F.Boat()
        b2 = self.F.Boat()
        form = self.get_massadmin_form(b1, b2)
        self.assertTrue("_mass_change_length_action" not in form.fields)

    def test_replace_floatfield(self):
        b1 = self.F.Boat()
        b2 = self.F.Boat()
        b3 = self.F.Boat()  # Will not be edited
        form = self.get_massadmin_form(b1, b2)
        self.update_form(form, length=13.2)
        form.submit().follow()
        self.assertEqual(Boat.objects.get(pk=b1.pk).length, 13.2)
        self.assertEqual(Boat.objects.get(pk=b2.pk).length, 13.2)
        self.assertEqual(Boat.objects.get(pk=b3.pk).length, b3.length)


class ForeignKeyTest(BaseTest):

    def test_no_action_available(self):
        # append, prepend, etc. makes no sense for a foreignkey
        b1 = self.F.Boat(name="Pen Duick")
        b2 = self.F.Boat(name="Pen Duick II")
        form = self.get_massadmin_form(b1, b2)
        self.assertTrue("_mass_change_captain_action" not in form.fields)

    def test_replace_foreignkey(self):
        c1 = self.F.Captain()
        c2 = self.F.Captain()
        c3 = self.F.Captain()
        b1 = self.F.Boat(captain=c1)
        b2 = self.F.Boat(captain=c2)
        b3 = self.F.Boat(captain=c1)  # Will not be edited
        # test Boats previous values
        self.assertEqual(Boat.objects.get(pk=b1.pk).captain, b1.captain)
        self.assertEqual(Boat.objects.get(pk=b2.pk).captain, b2.captain)
        form = self.get_massadmin_form(b1, b2)
        self.update_form(form, captain=c3.pk)
        form.submit().follow()
        self.assertEqual(Boat.objects.get(pk=b1.pk).captain, c3)
        self.assertEqual(Boat.objects.get(pk=b2.pk).captain, c3)
        self.assertEqual(Boat.objects.get(pk=b3.pk).captain, c1)


class ManyToManyFieldTest(BaseTest):

    def test_define_only_if_empty(self):
        c1 = self.F.Captain()
        c2 = self.F.Captain()
        c3 = self.F.Captain()
        b1 = self.F.Boat(captain=c1, previous_captains=[c2])
        b2 = self.F.Boat(captain=c2)
        b3 = self.F.Boat(captain=c1, previous_captains=[c3])  # Will not be edited
        # test Boats previous values
        self.assertEqual(Boat.objects.get(pk=b1.pk).captain, b1.captain)
        self.assertEqual(Boat.objects.get(pk=b2.pk).captain, b2.captain)
        form = self.get_massadmin_form(b1, b2)
        self.update_form(form, previous_captains=[c3.pk, c2.pk], previous_captains_action="define")
        form.submit().follow()
        self.assertEqual(set(Boat.objects.get(pk=b1.pk).previous_captains.all()), set([c2]))
        self.assertEqual(set(Boat.objects.get(pk=b2.pk).previous_captains.all()), set([c3, c2]))
        self.assertEqual(set(Boat.objects.get(pk=b3.pk).previous_captains.all()), set([c3]))

    def test_replace_manytomany(self):
        c1 = self.F.Captain()
        c2 = self.F.Captain()
        c3 = self.F.Captain()
        b1 = self.F.Boat(captain=c1, previous_captains=[c2])
        b2 = self.F.Boat(captain=c2)
        b3 = self.F.Boat(captain=c1, previous_captains=[c3])  # Will not be edited
        # test Boats previous values
        self.assertEqual(Boat.objects.get(pk=b1.pk).captain, b1.captain)
        self.assertEqual(Boat.objects.get(pk=b2.pk).captain, b2.captain)
        form = self.get_massadmin_form(b1, b2)
        self.update_form(form, previous_captains=[c3.pk, c2.pk], previous_captains_action="replace")
        form.submit().follow()
        self.assertEqual(set(Boat.objects.get(pk=b1.pk).previous_captains.all()), set([c3, c2]))
        self.assertEqual(set(Boat.objects.get(pk=b2.pk).previous_captains.all()), set([c3, c2]))
        self.assertEqual(set(Boat.objects.get(pk=b3.pk).previous_captains.all()), set([c3]))
