import uuid
import random
from datetime import datetime, timezone
from faker import Faker
from seed_data.config import supabase

fake = Faker("es_CO")

NAMESPACE = uuid.UUID("d0e1f2a3-b4c5-6789-defa-890123456789")

NUM_NOTIFICATIONS = 600

# Tipos y qué FK deben tener según la regla del schema
# AntExpenseAlert  → category_id
# GoalDeadlineReminder → goal_id
# BudgetExceeded   → category_id
# System           → todas nulas


def seed_notifications(users: list[dict], goals: list[dict],
                        movements: list[dict], categories: list[dict]) -> list[dict]:
    """
    Genera ~600 notificaciones respetando la regla:
    según el type, solo la FK correspondiente puede estar llena.
    """
    print("🔔 Generando notificaciones...")

    now = str(datetime.now(timezone.utc))
    notifications = []

    for i in range(NUM_NOTIFICATIONS):
        user  = random.choice(users)
        ntype = random.choice(["AntExpenseAlert", "GoalDeadlineReminder",
                               "BudgetExceeded", "System"])

        # FK según el tipo — regla de negocio del schema (chk_notification_entity)
        # AntExpenseAlert      → movement_id obligatorio
        # GoalDeadlineReminder → goal_id obligatorio
        # BudgetExceeded       → category_id obligatorio
        # System               → todas nulas
        goal_id     = None
        movement_id = None
        category_id = None

        if ntype == "AntExpenseAlert":
            if movements:
                movement_id = random.choice(movements)["id"]
            else:
                ntype = "System"  # fallback

        elif ntype == "GoalDeadlineReminder":
            user_goals = [g for g in goals if g["user_id"] == user["id"]]
            if user_goals:
                goal_id = random.choice(user_goals)["id"]
            else:
                ntype = "System"  # fallback si el usuario no tiene goals

        elif ntype == "BudgetExceeded":
            if categories:
                category_id = random.choice(categories)["id"]
            else:
                ntype = "System"  # fallback

        notifications.append({
            "id":          str(uuid.uuid5(NAMESPACE, f"notif-{i}")),
            "user_id":     user["id"],
            "type":        ntype,
            "title":       fake.sentence(nb_words=4).rstrip("."),
            "message":     fake.sentence(nb_words=10),
            "is_read":     random.choice([True, False]),
            "goal_id":     goal_id,
            "movement_id": movement_id,
            "category_id": category_id,
            "created_at":  now,
            "updated_at":  now,
        })

    inserted = []
    for i in range(0, len(notifications), 100):
        batch = notifications[i : i + 100]
        response = supabase.table("notifications").upsert(batch, on_conflict="id").execute()
        inserted.extend(response.data)

    print(f"   ✅ {len(inserted)} notificaciones insertadas.")
    return inserted
