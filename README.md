# ms-usuarios

Microservicio de **cuentas de acceso** del Sistema de Administracion de
Condominios: registro, inicio de sesion y administracion de usuarios.

> CS2032 Cloud Computing - UTEC | Proyecto: Sistema de Administracion de Condominios

## Responsable

[@Osomar1705](https://github.com/Osomar1705) — API con base de datos (Python).
Ver [INTEGRANTE.md](INTEGRANTE.md).

## Dominio

Es el **unico microservicio que emite tokens**. Guarda las cuentas con su
password hasheada y registra cada intento de inicio de sesion.

Los demas microservicios **no lo llaman**: verifican la firma de los tokens
localmente, usando el mismo `JWT_SECRET`. Si la firma cierra, confian en los
datos que el token trae adentro (id, email y rol).

```
                 ms-usuarios :9006  ──firma el token──►  el cliente lo guarda
                       │                                        │
                       │                                        ▼
                  PostgreSQL                    ms-residentes :9001 verifica
              condominio_usuarios               la firma con el MISMO secreto
                                                (sin llamar a ms-usuarios)
```

`usuarios.residente_id` es un **identificador logico** hacia ms-residentes: no
hay clave foranea ni llamada HTTP. El administrador lo tiene nulo porque no vive
en ninguna unidad.

## Stack

| Elemento | Tecnologia |
|----------|------------|
| Lenguaje | Python 3.12 |
| Framework | FastAPI |
| Base de datos | PostgreSQL 16 (base propia `condominio_usuarios`) |
| ORM | SQLAlchemy + psycopg |
| Passwords | bcrypt |
| Tokens | JWT (python-jose) |
| Documentacion | Swagger-UI en `/docs` |
| Contenedor | Docker |

**Tablas relacionadas:** `usuarios` <- `sesiones`.
Ver [docs/schema.sql](docs/schema.sql) y [docs/der.md](docs/der.md).

## Puerto asignado

**9006** publicado · **8000** dentro del contenedor.

| Microservicio | Publicado | Interno |
|---------------|-----------|---------|
| ms-residentes | 9001 | 8000 |
| ms-pagos | 9002 | 8080 |
| ms-incidencias | 9003 | 3003 |
| ms-ficha-residente | 9004 | 8004 |
| ms-analitico | 9005 | 8005 |
| ms-usuarios | **9006** | 8000 |
| web-condominio (dev) | 5173 | — |

## Endpoints REST

| # | Metodo | Ruta | Descripcion | Consumido por |
|---|--------|------|-------------|---------------|
| 1 | `POST` | `/auth/register` | Registra una cuenta y devuelve el token | **frontend** |
| 2 | `POST` | `/auth/login` | Autentica y devuelve el token | **frontend** |
| 3 | `GET` | `/auth/me` | Devuelve la cuenta duena del token | frontend |
| 4 | `GET` | `/usuarios` | Lista de cuentas (requiere token) | frontend |
| 5 | `POST` | `/usuarios` | Crea una cuenta (requiere rol ADMIN) | frontend |
| 6 | `DELETE` | `/usuarios/{usuario_id}` | Elimina una cuenta (requiere rol ADMIN) | frontend |
| 7 | `GET` | `/health` | Health check, comprueba tambien la BD | infra |

Los dos endpoints que consume directamente el **frontend** son
`POST /auth/login` y `POST /auth/register`.

Documentacion interactiva: `http://localhost:9006/docs`.

## Variables de entorno

| Variable | Descripcion | Ejemplo |
|----------|-------------|---------|
| `APP_NAME` | Nombre del servicio | `ms-usuarios` |
| `APP_PORT` | Puerto dentro del contenedor | `8000` |
| `PUBLISHED_PORT` | Puerto publicado en la VM | `9006` |
| `POSTGRES_HOST` | IP privada de la VM de base de datos | *(sin valor en el repo)* |
| `POSTGRES_PORT` | Puerto de PostgreSQL | `5432` |
| `POSTGRES_DB` | Nombre de la base | `condominio_usuarios` |
| `POSTGRES_USER` | Usuario de la base | *(sin valor en el repo)* |
| `POSTGRES_PASSWORD` | Password del usuario | *(sin valor en el repo)* |
| `JWT_SECRET` | Secreto de firma. **Tiene que ser el mismo en todos los microservicios** | *(sin valor en el repo)* |
| `JWT_ALGORITHM` | Algoritmo de firma | `HS256` |
| `JWT_EXPIRE_MINUTES` | Vigencia del token | `60` |

> El `JWT_SECRET` es el punto de contacto entre servicios: aca se firma, en los
> demas se verifica. Si no coincide, los tokens son rechazados en todos lados.
> Generarlo con `openssl rand -hex 32` y **nunca** commitearlo.

## Como levantar con Docker

```bash
cp .env.example .env
docker compose up -d --build
```

| Que | Donde |
|-----|-------|
| API | http://localhost:9006 |
| Swagger-UI | http://localhost:9006/docs |
| PostgreSQL desde tu maquina | `localhost:55433` |

Al arrancar por primera vez, PostgreSQL ejecuta
[docs/schema.sql](docs/schema.sql) y [docs/seed_data.sql](docs/seed_data.sql).

### Usuarios de prueba

Todos con la password **`condominio123`** (data de desarrollo):

| Email | Rol |
|-------|-----|
| `admin@condominio.com` | ADMIN |
| `lucia.vargas@example.com` | RESIDENTE |
| `ricardo.salazar@example.com` | RESIDENTE |
| `teresa.ampuero@example.com` | RESIDENTE |

### En la VM de produccion

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

La base `condominio_usuarios` se crea **dentro del contenedor PostgreSQL que ya
existe** en la VM de base de datos, al lado de `condominio_residentes`. Asi se
mantienen los 3 contenedores de base de datos que pidio el ACL. Los comandos
estan en los comentarios de [docker-compose.prod.yml](docker-compose.prod.yml).

## Coleccion de Postman

[postman/ms-usuarios.postman_collection.json](postman/ms-usuarios.postman_collection.json).
Correr `Login (admin)` primero: guarda el token en `{{token}}` y el resto de los
endpoints quedan autenticados solos.

## Estructura

```
app/
├── main.py       # instancia FastAPI
├── config.py     # lee y valida las variables de entorno
├── routers/      # auth (register/login/me) y usuarios (CRUD)
├── models/       # usuarios y sesiones
├── schemas/      # contratos de entrada y salida
├── security/     # hash bcrypt y emision de JWT
└── db/           # sesion y conexion a PostgreSQL
docs/
├── der.md, schema.sql, seed_data.sql
└── seed_fake_data.py   # carga de 20,000 registros (placeholder)
postman/
tests/
```

## Despliegue en AWS

Paso a paso en [DESPLIEGUE.md](DESPLIEGUE.md): crear la base en la VM de base de
datos, armar el `.env` en la VM de produccion y levantar los contenedores desde
Docker Hub.

## Estado

**Funcionando en local.** Register, login, `/auth/me` y CRUD de usuarios sobre
PostgreSQL, con registro de sesiones y datos de prueba cargados.

Pendiente: desplegar en la VM de produccion y publicar la imagen en Docker Hub.
