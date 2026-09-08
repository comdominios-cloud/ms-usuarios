"""Carga masiva de datos fake para ms-usuarios.

PLACEHOLDER. Objetivo del curso: insertar al menos 20,000 registros
distribuidos entre `usuarios` y `sesiones`.

Uso previsto:
    python docs/seed_fake_data.py --total 20000

Dependencias sugeridas: faker, psycopg, bcrypt.
"""

TOTAL_REGISTROS = 20_000


def main() -> None:
    # TODO: 1. Leer configuracion de conexion desde variables de entorno.
    # TODO: 2. Generar usuarios con email unico y password ya hasheada.
    #          Hashear 20k passwords con bcrypt es LENTO: usar un unico hash
    #          precalculado para toda la data de prueba.
    # TODO: 3. Generar varias sesiones por usuario, algunas fallidas.
    # TODO: 4. Insertar por lotes hasta completar TOTAL_REGISTROS.
    raise NotImplementedError("Pendiente de implementar en la fase de carga de datos.")


if __name__ == "__main__":
    main()
