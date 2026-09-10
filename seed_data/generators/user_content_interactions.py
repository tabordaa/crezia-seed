import uuid
import random
from datetime import datetime, timezone
from faker import Faker
from seed_data.config import supabase

fake = Faker("es_CO")

NAMESPACE = uuid.UUID("c9d0e1f2-a3b4-5678-cdef-789012345678")

NUM_INTERACTIONS = 500


def seed_user_content_interactions(users: list[dict],
                                   educational_content: list[dict]) -> list[dict]:
    """
    Genera ~500 interacciones usuario-contenido.
    Respeta el índice único: un usuario no puede interactuar dos veces
    con el mismo contenido.
    """
    print("👆 Generando interacciones de contenido...")

    now = datetime.now(timezone.utc)
    interactions = []
    used_pairs: set[tuple] = set()
    idx = 0

    # Pre-cargar pares existentes de la DB (re-ejecución)
    existing = supabase.table("user_content_interactions").select("user_id, content_id").execute().data
    for row in existing:
        used_pairs.add((row["user_id"], row["content_id"]))

    attempts = 0
    while len(interactions) < NUM_INTERACTIONS and attempts < NUM_INTERACTIONS * 5:
        attempts += 1
        user    = random.choice(users)
        content = random.choice(educational_content)
        pair    = (user["id"], content["id"])

        if pair in used_pairs:
            continue
        used_pairs.add(pair)

        is_read     = random.choice([True, False])
        is_rejected = False if is_read else random.choice([True, False])

        interactions.append({
            "id":         str(uuid.uuid5(NAMESPACE, f"interaction-{idx}")),
            "user_id":    user["id"],
            "content_id": content["id"],
            "is_favorite": random.choice([True, False]),
            "is_read":    is_read,
            "read_at":    str(fake.date_time_between(start_date="-6m", end_date="now", tzinfo=timezone.utc)) if is_read else None,
            "is_rejected": is_rejected,
            "rejected_at": str(fake.date_time_between(start_date="-6m", end_date="now", tzinfo=timezone.utc)) if is_rejected else None,
            "created_at": str(now),
            "updated_at": str(now),
        })
        idx += 1

    inserted = []
    for i in range(0, len(interactions), 100):
        batch = interactions[i : i + 100]
        response = supabase.table("user_content_interactions").upsert(batch, on_conflict="id").execute()
        inserted.extend(response.data)

    print(f"   ✅ {len(inserted)} interacciones insertadas.")
    return inserted
