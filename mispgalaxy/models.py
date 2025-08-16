from django.db import models

class ThreatActor(models.Model):
    uuid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=10, blank=True, null=True)
    attribution_confidence = models.IntegerField(blank=True, null=True)
    suspected_state_sponsor = models.CharField(max_length=100, blank=True, null=True)
    target_category = models.CharField(max_length=255, blank=True, null=True)
    incident_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class ThreatActorSynonym(models.Model):
    threat_actor = models.ForeignKey(
        ThreatActor, on_delete=models.CASCADE, related_name="synonyms"
    )
    synonym = models.CharField(max_length=255)

    def __str__(self):
        return self.synonym


class ThreatActorVictim(models.Model):
    threat_actor = models.ForeignKey(
        ThreatActor, on_delete=models.CASCADE, related_name="victims"
    )
    victim = models.CharField(max_length=255)

    def __str__(self):
        return self.victim


class ThreatActorReference(models.Model):
    threat_actor = models.ForeignKey(
        ThreatActor, on_delete=models.CASCADE, related_name="references"
    )
    reference_url = models.URLField(max_length=500)

    def __str__(self):
        return self.reference_url
