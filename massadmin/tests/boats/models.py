import datetime

from django.db import models
from django.contrib import admin

from massadmin.massadmin import MassAdmin


class Captain(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()


class Boat(models.Model):
    SLOOP = 1
    CUTTER = 2
    KETCH = 3
    SCHOONER = 4
    RIGGING = (
        (SLOOP, 'sloop'),
        (CUTTER, 'cutter'),
        (KETCH, 'ketch'),
        (SCHOONER, 'shooner'),
    )

    name = models.CharField(max_length=100)
    architect = models.CharField(max_length=100, null=True, blank=True)
    length = models.FloatField()
    rigging = models.SmallIntegerField(choices=RIGGING, default=SLOOP)

    captain = models.ForeignKey(Captain, related_name="boat")

    previous_captains = models.ManyToManyField(Captain, related_name="previous_boats")


class BoatAdmin(MassAdmin):
    pass
admin.site.register(Boat, BoatAdmin)


class Factory(object):

    def Boat(self, **kwargs):
        defaults = {
            "name": "Boat from factory",
            "length": 10
        }
        defaults.update(kwargs)
        if not "captain" in defaults:
            defaults.update({
                'captain': self.Captain()
            })
        previous_captains = defaults.pop("previous_captains", [])
        b = Boat(**defaults)
        b.save()
        if previous_captains:
            b.previous_captains.add(*previous_captains)
        return b

    def Captain(self, **kwargs):
        defaults = {
            "name": "Captain from factory",
            "birthday": datetime.datetime(1966, 3, 21)
        }
        defaults.update(kwargs)
        c = Captain(**defaults)
        c.save()
        return c
