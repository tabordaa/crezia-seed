import uuid
import random
from datetime import datetime, timezone
from faker import Faker
from seed_data.config import supabase

fake = Faker("es_CO")

NAMESPACE     = uuid.UUID("f2a3b4c5-d6e7-8901-fabc-012345678901")
PARSE_STATUSES = ["Pending", "Parsed", "Failed", "Ignored"]

NUM_EMAILS = 300


def seed_parsed_emails(email_connections: list[dict],
                        movements: list[dict]) -> list[dict]:
    """
    Genera ~300 emails parseados vinculados a conexiones de email.
    """
    print("📨 Generando emails parseados...")

    now = str(datetime.now(timezone.utc))
    parsed = []

    for i in range(NUM_EMAILS):
        connection   = random.choice(email_connections)
        parse_status = random.choices(
            PARSE_STATUSES, weights=[0.10, 0.65, 0.15, 0.10]
        )[0]

        # Solo los emails Parsed tienen movimiento asociado
        movement_id = None
        if parse_status == "Parsed" and movements:
            movement_id = random.choice(movements)["id"]

        parsed.append({
            "id":                  str(uuid.uuid5(NAMESPACE, f"parsed-email-{i}")),
            "email_connection_id": connection["id"],
            "external_message_id": fake.uuid4(),
            "sender_address":      fake.email(),
            "subject":             fake.sentence(nb_words=6) if random.random() > 0.20 else None,
            "received_at":         str(fake.date_time_between(start_date="-1y", end_date="now", tzinfo=timezone.utc)),
            "parse_status":        parse_status,
            "movement_id":         movement_id,
            "created_at":          now,
        })

    inserted = []
    for i in range(0, len(parsed), 100):
        batch = parsed[i : i + 100]
        response = supabase.table("parsed_emails").upsert(batch, on_conflict="id").execute()
        inserted.extend(response.data)

    print(f"   ✅ {len(inserted)} emails parseados insertados.")
    return inserted
