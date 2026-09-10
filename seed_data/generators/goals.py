import uuid
import random
from datetime import datetime, timezone, timedelta
from faker import Faker
from seed_data.config import supabase

fake = Faker("es_CO")

NAMESPACE = uuid.UUID("e5f6a7b8-c9d0-1234-efab-345678901234")

GOAL_STATUSES = ["Active", "Completed", "Cancelled", "Overdue"]
GOAL_REASONS  = ["Travel", "Vehicle", "Education", "EmergencyFund",
                  "HomePurchase", "Technology", "DebtPayment", "Other"]
CURRENCIES    = ["COP", "USD", "EUR", "GBP", "MXN"]

NUM_GOALS = 400


def seed_goals(users: list[dict], categories: list[dict]) -> list[dict]:
    """
    Genera ~400 metas de ahorro.
    Respeta el índice único: solo un goal Active/Overdue por (user_id, category_id).
    """
    print("🎯 Generando metas de ahorro...")

    now = datetime.now(timezone.utc)
    goals = []

    # Rastrea combinaciones (user_id, category_id) ya usadas con status activo
    # Incluye las que ya existen en la DB (re-ejecución)
    active_pairs: set[tuple] = set()

    existing = (
        supabase.table("goals")
        .select("user_id, category_id")
        .in_("status", ["Active", "Overdue"])
        .execute()
        .data
    )
    for g in existing:
        active_pairs.add((g["user_id"], g["category_id"]))

    # Solo usamos categorías globales para las metas (más realista)
    global_cats = [c for c in categories if c.get("user_id") is None]
    if not global_cats:
        global_cats = categories

    idx = 0
    attempts = 0

    while len(goals) < NUM_GOALS and attempts < NUM_GOALS * 5:
        attempts += 1
        user      = random.choice(users)
        category  = random.choice(global_cats)
        status    = random.choice(GOAL_STATUSES)

        pair = (user["id"], category["id"])

        # Regla: solo un Active/Overdue por (user_id, category_id)
        if status in ("Active", "Overdue") and pair in active_pairs:
            continue
        if status in ("Active", "Overdue"):
            active_pairs.add(pair)

        start_date = fake.date_between(start_date="-18m", end_date="today")
        end_date   = start_date + timedelta(days=random.randint(30, 720))
        target     = round(random.uniform(100_000, 50_000_000), 2)

        goals.append({
            "id":            str(uuid.uuid5(NAMESPACE, f"goal-{idx}")),
            "user_id":       user["id"],
            "category_id":   category["id"],
            "name":          fake.catch_phrase(),
            "reason":        random.choice(GOAL_REASONS),
            "target_amount": target,
            "currency_code": random.choice(CURRENCIES),
            "start_date":    str(start_date),
            "end_date":      str(end_date),
            "status":        status,
            "created_at":    str(now),
            "updated_at":    str(now),
        })
        idx += 1

    inserted = []
    for i in range(0, len(goals), 100):
        batch = goals[i : i + 100]
        response = supabase.table("goals").upsert(batch, on_conflict="id").execute()
        inserted.extend(response.data)

    print(f"   ✅ {len(inserted)} metas insertadas.")
    return inserted
