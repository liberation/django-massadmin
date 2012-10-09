import datetime

from django.db import models
from django.contrib import admin

from massadmin.massadmin import MassAdmin


class BaseModel(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s (%d)" % (self.name, self.pk)

    class Meta:
        abstract = True


class Captain(BaseModel):
    birthday = models.DateField()


class Race(BaseModel):
    pass


class Boat(BaseModel):
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

    architect = models.CharField(max_length=100, null=True, blank=True)
    length = models.FloatField()
    rigging = models.SmallIntegerField(choices=RIGGING, default=SLOOP)

    captain = models.ForeignKey(Captain, related_name="boat")

    previous_captains = models.ManyToManyField(Captain, related_name="previous_boats")
    win_races = models.ManyToManyField(Race, through="BoatToRace", related_name="winners")


class BoatToRace(models.Model):
    boat = models.ForeignKey(Boat)
    race = models.ForeignKey(Race)
    victory_date = models.DateField()


class BoatToRaceInline(admin.TabularInline):
    model = BoatToRace


class BoatAdmin(MassAdmin):
    inlines = (BoatToRaceInline, )
    exclude = ('win_races', )
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
        boattorace = defaults.pop("boattorace", [])
        b = Boat(**defaults)
        b.save()
        if previous_captains:
            b.previous_captains.add(*previous_captains)
        if boattorace:
            for race, victory_date in boattorace:
                if victory_date is None:
                    victory_date = datetime.datetime(2002, 2, 20)
                if isinstance(victory_date, str):
                    victory_date = datetime.strptime(victory_date, "Y/m/d")
                BoatToRace.objects.create(
                    boat=b,
                    race=race,
                    victory_date=victory_date
                )
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

    def Race(self, **kwargs):
        defaults = {
            "name": "Race from factory",
        }
        defaults.update(kwargs)
        c = Race(**defaults)
        c.save()
        return c
