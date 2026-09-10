import uuid
import random
from datetime import datetime, timezone
from faker import Faker
from seed_data.config import supabase

fake = Faker("es_CO")

NAMESPACE = uuid.UUID("c3d4e5f6-a7b8-9012-cdef-123456789012")

ACCOUNT_TYPES = ["Savings", "Checking", "Credit", "Other"]
CURRENCIES     = ["COP", "USD", "EUR", "GBP", "MXN"]
BANKS = [
    "Bancolombia", "Davivienda", "Banco de Bogotá", "BBVA",
    "Nequi", "Daviplata", "Banco Popular", "Colpatria",
    "Scotiabank", "Itaú", "Banco Agrario", "Caja Social",
]


def seed_bank_accounts(users: list[dict]) -> list[dict]:
    """
    Genera 1-2 cuentas bancarias por usuario (~600 en total).
    """
    print("🏦 Generando cuentas bancarias...")

    now = str(datetime.now(timezone.utc))
    accounts = []
    idx = 0

    for user in users:
        num_accounts = random.choices([1, 2], weights=[0.6, 0.4])[0]
        for _ in range(num_accounts):
            accounts.append({
                "id":           str(uuid.uuid5(NAMESPACE, f"account-{idx}")),
                "user_id":      user["id"],
                "bank_name":    random.choice(BANKS),
                "account_alias": fake.word().capitalize() if random.random() > 0.20 else None,
                "account_type": random.choice(ACCOUNT_TYPES),
                "currency_code": random.choice(CURRENCIES),
                "last_synced_at": str(fake.date_time_between(start_date="-3m", end_date="now", tzinfo=timezone.utc)) if random.random() > 0.40 else None,
                "created_at":   now,
                "updated_at":   now,
            })
            idx += 1

    inserted = []
    for i in range(0, len(accounts), 100):
        batch = accounts[i : i + 100]
        response = supabase.table("bank_accounts").upsert(batch, on_conflict="id").execute()
        inserted.extend(response.data)

    print(f"   ✅ {len(inserted)} cuentas bancarias insertadas.")
    return inserted
