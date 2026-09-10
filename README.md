# 🌱 Crezia — Seed Data Generator

Script de Python para generar datos sintéticos en la base de datos de **Crezia**,
una app de finanzas personales. Los datos generados son intencionalmente imperfectos
(nulos, formatos erróneos, valores fuera de rango) para practicar procesos de **ETL**
en el contexto de la materia de Business Intelligence.

## 📋 Contexto académico

- **Materia:** Business Intelligence
- **Actividad:** TIA 2 — Consultas SQL y análisis de datos
- **Dataset:** Generado sintéticamente sobre el schema real de Crezia en Supabase

## 🗂️ Estructura del proyecto

    crezia-seed/
    ├── seed_data/
    │   ├── config.py            ← Cliente Supabase
    │   ├── generators/          ← Un archivo por tabla
    │   └── main.py              ← Orquestador principal
    ├── .env.example             ← Plantilla de credenciales
    ├── requirements.txt         ← Dependencias
    └── README.md

## ⚙️ Instalación

1. Clona el repositorio
2. Crea tu archivo `.env` basado en `.env.example`
3. Instala las dependencias:

    pip install -r requirements.txt

4. Ejecuta el script:

    python -m seed_data.main

## 👥 Equipo

- Kevin Taborda
- Anyi Manco