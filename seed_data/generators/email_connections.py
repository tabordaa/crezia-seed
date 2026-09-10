import uuid
import random
from datetime import datetime, timezone
from faker import Faker
from seed_data.config import supabase

fake = Faker("es_CO")

NAMESPACE  = uuid.UUID("e1f2a3b4-c5d6-7890-efab-901234567890")
PROVIDERS  = ["Gmail", "Outlook"]

NUM_CONNECTIONS = 200


def seed_email_connections(users: list[dict]) -> list[dict]:
    """
    Genera ~200 conexiones de email (una por usuario en una muestra).
    Respeta el índice único: un usuario no puede tener dos conexiones
    con el mismo email_address.
    """
    print("📧 Generando conexiones de email...")

    now = str(datetime.now(timezone.utc))
    connections = []
    used_pairs: set[tuple] = set()

    sample_users = random.sample(users, min(NUM_CONNECTIONS, len(users)))

    for i, user in enumerate(sample_users):
        email_address = fake.email()
        pair = (user["id"], email_address)

        # Garantizar unicidad (user_id, email_address)
        if pair in used_pairs:
            email_address = f"alt.{i}.{email_address}"
        used_pairs.add((user["id"], email_address))

        connections.append({
            "id":                      str(uuid.uuid5(NAMESPACE, f"email-conn-{i}")),
            "user_id":                 user["id"],
            "provider":                random.choice(PROVIDERS),
            "email_address":           email_address,
            "access_token_encrypted":  fake.sha256(),
            "refresh_token_encrypted": fake.sha256(),
            "scope":                   "https://mail.google.com/",
            "is_active":               random.choice([True, False]),
            "last_synced_at":          str(fake.date_time_between(start_date="-30d", end_date="now", tzinfo=timezone.utc)) if random.random() > 0.30 else None,
            "connected_at":            str(fake.date_time_between(start_date="-1y", end_date="now", tzinfo=timezone.utc)),
            "created_at":              now,
            "updated_at":              now,
        })

    response = supabase.table("email_connections").upsert(connections, on_conflict="id").execute()
    print(f"   ✅ {len(response.data)} conexiones de email insertadas.")
    return response.data
