"""
main.py — Orquestador del seed de datos de Crezia.

Ejecuta cada generador en orden respetando las dependencias
de Foreign Keys entre tablas.

Uso:
    python -m seed_data.main
"""

from seed_data.generators.currencies              import seed_currencies
from seed_data.generators.users                   import seed_users
from seed_data.generators.categories              import seed_categories
from seed_data.generators.bank_accounts           import seed_bank_accounts
from seed_data.generators.financial_profiles      import seed_financial_profiles
from seed_data.generators.goals                   import seed_goals
from seed_data.generators.movements               import seed_movements
from seed_data.generators.content_categories      import seed_content_categories
from seed_data.generators.educational_content     import seed_educational_content
from seed_data.generators.user_content_interactions import seed_user_content_interactions
from seed_data.generators.notifications           import seed_notifications
from seed_data.generators.email_connections       import seed_email_connections
from seed_data.generators.parsed_emails           import seed_parsed_emails


def main():
    print("\n🌱 Iniciando seed de datos — Crezia BI\n" + "=" * 45)

    # 1. Sin dependencias
    currencies         = seed_currencies()

    # 2. Depende de currency
    users              = seed_users()

    # 3. Depende de users
    categories         = seed_categories(users)
    bank_accounts      = seed_bank_accounts(users)
    financial_profiles = seed_financial_profiles(users)

    # 4. Depende de users + categories + currency
    goals              = seed_goals(users, categories)

    # 5. Depende de users + bank_accounts + categories
    movements          = seed_movements(users, bank_accounts, categories)

    # 6. Contenido educativo — sin dependencia de usuarios
    content_categories = seed_content_categories()
    edu_content        = seed_educational_content(content_categories)

    # 7. Depende de users + contenido
    seed_user_content_interactions(users, edu_content)

    # 8. Depende de users + goals + movements + categories
    seed_notifications(users, goals, movements, categories)

    # 9. Depende de users
    email_connections  = seed_email_connections(users)

    # 10. Depende de email_connections + movements
    seed_parsed_emails(email_connections, movements)

    print("\n" + "=" * 45)
    print("✅ Seed completado exitosamente.")


if __name__ == "__main__":
    main()
