import uuid
import random
from datetime import datetime, timezone
from faker import Faker
from seed_data.config import supabase

fake = Faker("es_CO")

NAMESPACE      = uuid.UUID("b8c9d0e1-f2a3-4567-bcde-678901234567")
CONTENT_TYPES  = ["Article", "Video", "Tip", "Infographic"]
CONTENT_STATUS = ["Draft", "Published", "Archived"]

NUM_CONTENT = 50


def seed_educational_content(content_categories: list[dict]) -> list[dict]:
    """Genera ~50 piezas de contenido educativo."""
    print("🎓 Generando contenido educativo...")

    now = datetime.now(timezone.utc)
    content = []

    for i in range(NUM_CONTENT):
        category  = random.choice(content_categories)
        ctype     = random.choice(CONTENT_TYPES)
        status    = random.choices(CONTENT_STATUS, weights=[0.15, 0.70, 0.15])[0]

        content.append({
            "id":                  str(uuid.uuid5(NAMESPACE, f"edu-{i}")),
            "content_category_id": category["id"],
            "title":               fake.catch_phrase(),
            "type":                ctype,
            "body":                fake.paragraph(nb_sentences=5) if ctype in ("Article", "Tip") else None,
            "media_url":           f"https://cdn.crezia.app/{uuid.uuid4()}.mp4" if ctype == "Video" else None,
            "duration_minutes":    random.randint(2, 30) if ctype == "Video" else None,
            "status":              status,
            "published_at":        str(fake.date_time_between(start_date="-1y", end_date="now", tzinfo=timezone.utc)) if status == "Published" else None,
            "created_at":          str(now),
            "updated_at":          str(now),
        })

    response = supabase.table("educational_content").upsert(content, on_conflict="id").execute()
    print(f"   ✅ {len(response.data)} contenidos educativos insertados.")
    return response.data
