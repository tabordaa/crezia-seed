from seed_data.config import supabase


# 5 currencies to use

CURRENCIES = [

    {
        "code": "COP",
        "name":  "Peso colombiano",
        "symbol": "$",
        "decimal_places": 0,
        "is_active": True
    },
    {
        "code": "USD",
        "name":  "Dólar estadounidense",
        "symbol": "$",
        "decimal_places": 2,
        "is_active": True
    },
    {
        "code": "EUR",
        "name":  "Euro",
        "symbol": "€",
        "decimal_places": 2,
        "is_active": True
    },
    {
        "code": "GBP",
        "name":  "Libra esterlina",
        "symbol": "£",
        "decimal_places": 2,
        "is_active": True
    },
    {
        "code": "MXN",
        "name":  "Peso mexicano",
        "symbol": "$",
        "decimal_places": 2,
        "is_active": False
    }
]


def seed_currencies() -> list[dict]:
    """
    Inserts currencies in currency table
    Uses upsert on 'code'
    Returns list of currencies
    """

    print("Insertando monedas")

    response = (
        supabase.table("currency")
        .upsert(CURRENCIES,on_conflict="code")
        .execute()
    )

    print(f"{len(response.data)} monedas insertadas")
    return response.data