import random
from datetime import datetime, timezone
from faker import Faker
from seed_data.config import supabase

fake = Faker("es_CO")

GENDERS   = ["Female", "Male", "Other"]
CURRENCIES = ["COP", "USD", "EUR", "GBP", "MXN"]

NUM_USERS = 100


def seed_users() -> list[dict]:
    """
    Crea usuarios en auth.users (via admin API) y luego en public.users.
    Si ya existen (re-ejecución), los recupera de public.users.
    """
    print(f"👤 Generando {NUM_USERS} usuarios (auth + public)...")

    public_users = []
    created_count = 0

    for i in range(NUM_USERS):
        auth_email = f"crezia.seed.{i}@crezia-bi.dev"

        try:
            auth_response = supabase.auth.admin.create_user({
                "email": auth_email,
                "password": "SeedPassword123!",
                "email_confirm": True,
            })
            user_id = auth_response.user.id
            created_count += 1

        except Exception as e:
            if "already been registered" in str(e):
                continue  # Lo recuperamos después de la DB
            else:
                print(f"   ⚠️  Error creando usuario {i} en auth: {e}")
                continue

        deleted_at = (
            str(fake.date_time_between(start_date="-6m", end_date="now", tzinfo=timezone.utc))
            if random.random() < 0.05
            else None
        )

        public_users.append({
            "id":                      user_id,
            "document_id":             fake.numerify("##########"),
            "name":                    fake.name(),
            "email":                   auth_email,
            "birth_date":              str(fake.date_of_birth(minimum_age=18, maximum_age=70)),
            "address":                 fake.address() if random.random() > 0.20 else None,
            "phone":                   fake.numerify("3#########") if random.random() > 0.20 else None,
            "gender":                  random.choice(GENDERS) if random.random() > 0.20 else None,
            "role":                    "Admin" if i < 5 else "User",
            "preferred_currency_code": random.choice(CURRENCIES),
            "two_factor_enabled":      random.choice([True, False]),
            "created_at":              str(fake.date_time_between(start_date="-2y", end_date="now", tzinfo=timezone.utc)),
            "updated_at":              str(datetime.now(timezone.utc)),
            "deleted_at":              deleted_at,
        })

        if (i + 1) % 10 == 0:
            print(f"   Auth: {i + 1}/{NUM_USERS} usuarios creados...")

    # Insertar nuevos en public.users
    if public_users:
        for i in range(0, len(public_users), 50):
            batch = public_users[i : i + 50]
            supabase.table("users").upsert(batch, on_conflict="id").execute()
        print(f"   ✅ {len(public_users)} usuarios nuevos insertados.")
    else:
        print(f"   ↩️  Todos los usuarios ya existían en auth.")

    # Siempre recuperar la lista completa de public.users para los demás generadores
    all_users = supabase.table("users").select("*").execute().data
    print(f"   📋 {len(all_users)} usuarios totales en public.users.")
    return all_users