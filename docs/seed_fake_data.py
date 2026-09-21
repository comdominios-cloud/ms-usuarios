"""Carga masiva de datos ficticios para ms-usuarios (PostgreSQL).

El curso pide minimo 20,000 registros en al menos una tabla de cada base.
Aca la tabla masiva es `usuarios`, y se generan tambien sus `sesiones`.

Uso:
    python docs/seed_fake_data.py                 # 20,000 usuarios
    python docs/seed_fake_data.py --total 50000
    python docs/seed_fake_data.py --limpiar

Sobre el hash de las passwords: bcrypt tarda a proposito (unos 100 ms por
password con coste 12). Hashear 20,000 llevaria mas de media hora. Como son
datos de prueba y todos comparten la misma password, se calcula **un solo
hash** y se reutiliza. En datos reales cada password tiene su propio salt,
que es justamente lo que hace bcrypt por defecto.

Dependencias:
    pip install faker psycopg[binary] python-dotenv bcrypt
"""

import argparse
import os
import random
import sys
from datetime import datetime, timedelta

try:
    import bcrypt
    import psycopg
    from dotenv import load_dotenv
    from faker import Faker
except ImportError as e:
    sys.exit(f"Falta una dependencia: {e}\n  pip install faker psycopg[binary] python-dotenv bcrypt")

TOTAL_POR_DEFECTO = 20_000
LOTE = 5_000
PASSWORD_DEMO = "condominio123"
SESIONES_POR_USUARIO = 2

NAVEGADORES = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 14)",
)

fake = Faker("es_ES")
Faker.seed(2026)
random.seed(2026)


def conexion():
    load_dotenv()
    faltantes = [
        v for v in ("POSTGRES_HOST", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD")
        if not os.getenv(v)
    ]
    if faltantes:
        sys.exit(f"Faltan variables de entorno: {', '.join(faltantes)}")

    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def limpiar(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM sesiones")
        cur.execute("DELETE FROM usuarios")
        cur.execute("ALTER SEQUENCE sesiones_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE usuarios_id_seq RESTART WITH 1")
    conn.commit()
    print("  Tablas vaciadas")


def insertar_usuarios(conn, total: int, hash_password: str) -> list[int]:
    emails: set[str] = set()
    insertados = 0
    hoy = datetime.now()

    with conn.cursor() as cur:
        while insertados < total:
            cantidad = min(LOTE, total - insertados)
            lote = []

            while len(lote) < cantidad:
                n = insertados + len(lote) + 1
                email = f"{fake.user_name()}{n}@example.com"
                if email in emails:
                    continue
                emails.add(email)

                creado = hoy - timedelta(days=random.randint(0, 1460))
                # Solo algunos tienen ultimo_login: los demas nunca entraron.
                ultimo = (
                    creado + timedelta(days=random.randint(0, 200))
                    if random.random() > 0.3
                    else None
                )

                lote.append(
                    (
                        random.randint(1, total) if random.random() > 0.02 else None,
                        email[:160],
                        hash_password,
                        "ADMIN" if random.random() < 0.01 else "RESIDENTE",
                        random.random() > 0.05,
                        ultimo,
                        creado,
                    )
                )

            with cur.copy(
                "COPY usuarios "
                "(residente_id, email, password_hash, rol, activo, ultimo_login, creado_en) "
                "FROM STDIN"
            ) as copia:
                for fila in lote:
                    copia.write_row(fila)

            conn.commit()
            insertados += cantidad
            print(f"  usuarios: {insertados:>7,} / {total:,}", end="\r", flush=True)

        cur.execute("SELECT id FROM usuarios ORDER BY id")
        ids = [r[0] for r in cur.fetchall()]

    print(f"  usuarios: {insertados:>7,} insertados          ")
    return ids


def insertar_sesiones(conn, usuarios: list[int]) -> None:
    hoy = datetime.now()
    total = len(usuarios) * SESIONES_POR_USUARIO
    insertados = 0

    with conn.cursor() as cur:
        for inicio in range(0, len(usuarios), LOTE):
            trozo = usuarios[inicio : inicio + LOTE]
            lote = []

            for usuario_id in trozo:
                for _ in range(SESIONES_POR_USUARIO):
                    lote.append(
                        (
                            usuario_id,
                            hoy - timedelta(minutes=random.randint(0, 525_600)),
                            fake.ipv4(),
                            random.choice(NAVEGADORES),
                            random.random() > 0.15,  # 15% de intentos fallidos
                        )
                    )

            with cur.copy(
                "COPY sesiones (usuario_id, inicio, ip_origen, user_agent, exitoso) "
                "FROM STDIN"
            ) as copia:
                for fila in lote:
                    copia.write_row(fila)

            conn.commit()
            insertados += len(lote)
            print(f"  sesiones: {insertados:>7,} / {total:,}", end="\r", flush=True)

    print(f"  sesiones: {insertados:>7,} insertadas          ")


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga masiva para ms-usuarios")
    parser.add_argument("--total", type=int, default=TOTAL_POR_DEFECTO)
    parser.add_argument("--limpiar", action="store_true")
    parser.add_argument("--sin-sesiones", action="store_true",
                        help="Solo la tabla usuarios")
    args = parser.parse_args()

    print(f"Generando {args.total:,} usuarios")
    print(f"  password de todos: {PASSWORD_DEMO}")

    print("  calculando el hash (una sola vez)...", end=" ", flush=True)
    hash_password = bcrypt.hashpw(PASSWORD_DEMO.encode(), bcrypt.gensalt(rounds=12)).decode()
    print("listo")

    with conexion() as conn:
        if args.limpiar:
            limpiar(conn)

        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM usuarios")
            existentes = cur.fetchone()[0]

        if existentes and not args.limpiar:
            print(f"  Aviso: ya hay {existentes:,} usuarios. Se agregan encima.")

        usuarios = insertar_usuarios(conn, args.total, hash_password)

        if not args.sin_sesiones:
            insertar_sesiones(conn, usuarios)

        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM usuarios")
            u = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM sesiones")
            s = cur.fetchone()[0]
            print(f"\nTotales: usuarios {u:,} | sesiones {s:,}")


if __name__ == "__main__":
    main()
