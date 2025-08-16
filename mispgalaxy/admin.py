from django.contrib import admin
from .models import ThreatActor, ThreatActorSynonym, ThreatActorVictim, ThreatActorReference

class ThreatActorSynonymInline(admin.TabularInline):
    model = ThreatActorSynonym
    extra = 1


class ThreatActorVictimInline(admin.TabularInline):
    model = ThreatActorVictim
    extra = 1


class ThreatActorReferenceInline(admin.TabularInline):
    model = ThreatActorReference
    extra = 1


@admin.register(ThreatActor)
class ThreatActorAdmin(admin.ModelAdmin):
    list_display = ("name", "uuid", "country", "suspected_state_sponsor", "attribution_confidence")
    list_filter = ("country", "suspected_state_sponsor")
    search_fields = ("name", "uuid", "country", "suspected_state_sponsor", "synonyms__synonym")
    inlines = [ThreatActorSynonymInline, ThreatActorVictimInline, ThreatActorReferenceInline]
    ordering = ("name",)


@admin.register(ThreatActorSynonym)
class ThreatActorSynonymAdmin(admin.ModelAdmin):
    list_display = ("synonym", "threat_actor")
    search_fields = ("synonym", "threat_actor__name")


@admin.register(ThreatActorVictim)
class ThreatActorVictimAdmin(admin.ModelAdmin):
    list_display = ("victim", "threat_actor")
    search_fields = ("victim", "threat_actor__name")


@admin.register(ThreatActorReference)
class ThreatActorReferenceAdmin(admin.ModelAdmin):
    list_display = ("reference_url", "threat_actor")
    search_fields = ("reference_url", "threat_actor__name")
