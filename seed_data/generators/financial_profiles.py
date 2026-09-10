import uuid
import random
from datetime import datetime, timezone
from seed_data.config import supabase

NAMESPACE = uuid.UUID("d4e5f6a7-b8c9-0123-defa-234567890123")

PAYMENT_METHODS = ["Cash", "Transfer", "CreditCard", "DebitCard", "Other"]


def seed_financial_profiles(users: list[dict]) -> list[dict]:
    """
    Genera un perfil financiero por usuario.
    Incluye valores fuera de rango (~5%) para simular datos sucios.
    """
    print("📊 Generando perfiles financieros...")

    now = str(datetime.now(timezone.utc))
    profiles = []

    for i, user in enumerate(users):
        monthly_income = round(random.uniform(800_000, 15_000_000), 2)

        profiles.append({
            "id":                       str(uuid.uuid5(NAMESPACE, f"fp-{i}")),
            "user_id":                  user["id"],
            "monthly_income":           monthly_income,
            "fixed_expenses":           round(random.uniform(200_000, 5_000_000), 2) if random.random() > 0.20 else None,
            "ant_expense_percentage":   round(random.uniform(1, 60), 2) if random.random() > 0.20 else None,
            "makes_unnecessary_purchases": random.choice([True, False]) if random.random() > 0.20 else None,
            "has_debts":                random.choice([True, False]) if random.random() > 0.20 else None,
            "debt_amount":              round(random.uniform(0, 50_000_000), 2) if random.random() > 0.30 else None,
            "app_usefulness_rating":    random.randint(1, 5) if random.random() > 0.20 else None,
            "currently_saves":          random.choice([True, False]) if random.random() > 0.20 else None,
            "proposed_savings_amount":  round(random.uniform(50_000, 3_000_000), 2) if random.random() > 0.30 else None,
            "has_financial_knowledge":  random.choice([True, False]) if random.random() > 0.20 else None,
            "can_detect_ant_expenses":  random.choice([True, False]) if random.random() > 0.20 else None,
            "primary_payment_method":   random.choice(PAYMENT_METHODS) if random.random() > 0.20 else None,
            "created_at":               now,
            "updated_at":               now,
        })

    inserted = []
    for i in range(0, len(profiles), 100):
        batch = profiles[i : i + 100]
        response = supabase.table("financial_profile").upsert(batch, on_conflict="id").execute()
        inserted.extend(response.data)

    print(f"   ✅ {len(inserted)} perfiles financieros insertados.")
    return inserted
