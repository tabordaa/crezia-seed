import uuid
import random
from datetime import datetime, timezone
from faker import Faker
from seed_data.config import supabase

fake = Faker("es_CO")

NAMESPACE = uuid.UUID("b2c3d4e5-f6a7-8901-bcde-f12345678901")

# fixed global categories
GLOBAL_CATEGORIES = [
 "Alimentación",
 "Transporte",
 "Arriendo",
 "Salud",
 "Educación",
 "Entretenimiento",
 "Ropa",
 "Servicios públicos",
 "Tecnología",
 "Restaurantes",
 "Viajes",
 "Deporte",
 "Mascotas",
 "Regalos",
 "Ahorros",
 "Inversiones",
 "Salario",
 "Freelance",
 "Arriendos recibidos",
 "Otros"
]


# Personal options users might create
PERSONAL_OPTIONS = [
    "Suscripciones",
    "Café",
    "Delivery",
    "Juegos",
    "Libros",
    "Cursos online",
    "Gimnasio",
    "Belleza",
    "Farmacia",
    "Supermercado",
    "Gasolina",
    "Parqueadero",
    "Mesada",
    "Propinas",
    "Ventas personales",
    "Bonos"
]

NUM_PERSONAL = 200

def seed_categories(users: list[dict]) -> list[dict]:
    """
    Inserts fixed and personal categories
    Receives a users list to asign user_id to personal categories
    Returns inserted categories
    """

    print("Generando categorías")

    now = str(datetime.now(timezone.utc))
    categories = []

    # Global categories
    for i, name in enumerate(GLOBAL_CATEGORIES):
        categories.append({
            "id": str(uuid.uuid5(NAMESPACE,f"global-cat-{i}")),
            "user_id": None, # Available for all users
            "name": name,
            "description": fake.sentence(nb_words=6) if random.random() > 0.30 else None,
            "is_default": True,
            "created_at": now,
            "updated_at": now
        })

    # Personal categories
    # Take a random sample of users to assign them personal categories
    sample_users = random.sample(users, min(NUM_PERSONAL, len(users)))

    for i, user in enumerate(sample_users):
        categories.append({
            "id": str(uuid.uuid5(NAMESPACE,f"personal-cat-{i}")),
            "user_id": user["id"],
            "name": random.choice(PERSONAL_OPTIONS),
            "description": fake.sentence(nb_words=5) if random.random() > 0.30 else None,
            "is_default": False,
            "created_at": now,
            "updated_at": now
        })

    # Inserts lots of 100
    inserted = []
    for i in range(0,len(categories),100):
        batch = categories[i : i + 100]
        response = supabase.table("categories").upsert(batch,on_conflict="id").execute()
        inserted.extend(response.data)


    print(f"{len(inserted)} categorías insertadas ({len(GLOBAL_CATEGORIES)} globales, {len(NUM_PERSONAL)} personales.)")
    return inserted