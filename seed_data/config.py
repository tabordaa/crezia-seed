import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load variables from .env file
load_dotenv()

# Read credentials
SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY")

# Checks if credentials exists
if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise ValueError(
        "Faltan las credenciales. Asegurate de tener SUPABASE_URL y SUPABASE_SERVICE_KEY en el archivo .env"
    )

# Creates supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)