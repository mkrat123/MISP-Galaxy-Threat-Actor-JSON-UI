import json
from django.core.management.base import BaseCommand
from mispgalaxy.models import ThreatActor, ThreatActorSynonym, ThreatActorVictim, ThreatActorReference

class Command(BaseCommand):
    help = "Import Threat Actors from MISP-Galaxy threat-actor.json file"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to threat-actor.json file")

    def handle(self, *args, **options):
        json_file = options["json_file"]

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading JSON file: {e}"))
            return

        actors_data = data.get("values", [])
        count = 0

        for entry in actors_data:
            meta = entry.get("meta", {})
            actor, created = ThreatActor.objects.get_or_create(
                uuid=entry.get("uuid"),
                defaults={
                    "name": entry.get("value", ""),
                    "description": entry.get("description", ""),
                    "country": meta.get("country", ""),
                    "attribution_confidence": int(meta.get("attribution-confidence", 0)) if meta.get("attribution-confidence") else None,
                    "suspected_state_sponsor": meta.get("cfr-suspected-state-sponsor", ""),
                    "target_category": ", ".join(meta.get("cfr-target-category", [])),
                    "incident_type": meta.get("cfr-type-of-incident", "")
                }
            )

            if created:
                # Synonyms
                for synonym in meta.get("synonyms", []):
                    ThreatActorSynonym.objects.create(threat_actor=actor, synonym=synonym)

                # Victims
                for victim in meta.get("cfr-suspected-victims", []):
                    ThreatActorVictim.objects.create(threat_actor=actor, victim=victim)

                # References
                for ref in meta.get("refs", []):
                    ThreatActorReference.objects.create(threat_actor=actor, reference_url=ref)

                count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {count} new threat actors from {json_file}"))
