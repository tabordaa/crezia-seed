import uuid
from datetime import datetime, timezone
from seed_data.config import supabase

NAMESPACE = uuid.UUID("a7b8c9d0-e1f2-3456-abcd-567890123456")

CONTENT_CATEGORIES = [
    {"name": "Ahorro",             "description": "Estrategias y hábitos de ahorro personal"},
    {"name": "Inversiones",        "description": "Conceptos básicos y avanzados de inversión"},
    {"name": "Deudas",             "description": "Cómo manejar y eliminar deudas"},
    {"name": "Presupuesto",        "description": "Planificación y control del presupuesto"},
    {"name": "Gastos hormiga",     "description": "Identificación y control de pequeños gastos frecuentes"},
    {"name": "Metas financieras",  "description": "Cómo definir y alcanzar objetivos de dinero"},
    {"name": "Crédito",            "description": "Uso responsable del crédito y tarjetas"},
    {"name": "Educación financiera", "description": "Conceptos fundamentales de finanzas personales"},
]


def seed_content_categories() -> list[dict]:
    """Inserta las categorías de contenido educativo."""
    print("📚 Generando categorías de contenido...")

    now = str(datetime.now(timezone.utc))
    records = []

    for i, cat in enumerate(CONTENT_CATEGORIES):
        records.append({
            "id":          str(uuid.uuid5(NAMESPACE, f"content-cat-{i}")),
            "name":        cat["name"],
            "description": cat["description"],
            "created_at":  now,
            "updated_at":  now,
        })

    response = supabase.table("content_categories").upsert(records, on_conflict="id").execute()
    print(f"   ✅ {len(response.data)} categorías de contenido insertadas.")
    return response.data
