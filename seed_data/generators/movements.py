import uuid
import random
from datetime import datetime, timezone
from faker import Faker
from seed_data.config import supabase

fake = Faker("es_CO")

NAMESPACE       = uuid.UUID("f6a7b8c9-d0e1-2345-fabc-456789012345")
MOVEMENT_TYPES  = ["Income", "Expense"]
PAYMENT_METHODS = ["Cash", "Transfer", "CreditCard", "DebitCard", "Other"]
SOURCES         = ["Manual", "EmailParsed"]
CURRENCIES      = ["COP", "USD", "EUR", "GBP", "MXN"]

NUM_MOVEMENTS = 2000


def _dirty_amount() -> float:
    """Retorna un monto fuera de rango para simular datos sucios."""
    return random.choice([-999, -1, 0, -50000])


def seed_movements(users: list[dict], bank_accounts: list[dict],
                   categories: list[dict]) -> list[dict]:
    """
    Genera ~2000 movimientos financieros.
    Incluye ~5% de montos fuera de rango y ~20% sin cuenta bancaria.
    """
    print("💸 Generando movimientos...")

    now = datetime.now(timezone.utc)
    movements = []

    # Índice para buscar cuentas por user_id rápidamente
    accounts_by_user: dict[str, list] = {}
    for acc in bank_accounts:
        accounts_by_user.setdefault(acc["user_id"], []).append(acc)

    for i in range(NUM_MOVEMENTS):
        user     = random.choice(users)
        category = random.choice(categories)

        # Cuenta bancaria: 80% tiene una asignada, 20% no
        user_accounts = accounts_by_user.get(user["id"], [])
        bank_account_id = (
            random.choice(user_accounts)["id"]
            if user_accounts and random.random() > 0.20
            else None
        )

        # Monto: 5% con valor sucio
        if random.random() < 0.05:
            amount = _dirty_amount()
        else:
            amount = round(random.uniform(5_000, 10_000_000), 2)

        movements.append({
            "id":              str(uuid.uuid5(NAMESPACE, f"mov-{i}")),
            "user_id":         user["id"],
            "bank_account_id": bank_account_id,
            "category_id":     category["id"],
            "type":            random.choice(MOVEMENT_TYPES),
            "amount":          amount,
            "currency_code":   random.choice(CURRENCIES),
            "date":            str(fake.date_between(start_date="-2y", end_date="today")),
            "payment_method":  random.choice(PAYMENT_METHODS),
            "source":          random.choice(SOURCES),
            "description":     fake.sentence(nb_words=5) if random.random() > 0.20 else None,
            "created_at":      str(now),
            "updated_at":      str(now),
        })

    inserted = []
    for i in range(0, len(movements), 100):
        batch = movements[i : i + 100]
        response = supabase.table("movements").upsert(batch, on_conflict="id").execute()
        inserted.extend(response.data)

    print(f"   ✅ {len(inserted)} movimientos insertados.")
    return inserted
