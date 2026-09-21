# Diagrama Entidad-Relacion — ms-usuarios

Base: **PostgreSQL** · `condominio_usuarios`

```mermaid
erDiagram
    USUARIOS ||--o{ SESIONES : "registra"

    USUARIOS {
        bigserial id PK
        bigint residente_id "id logico hacia ms-residentes, NULL en el admin"
        varchar(160) email "UNIQUE"
        varchar(255) password_hash "bcrypt, nunca la password en claro"
        varchar(20) rol "ADMIN | RESIDENTE"
        boolean activo
        timestamp ultimo_login
        timestamp creado_en
    }

    SESIONES {
        bigserial id PK
        bigint usuario_id FK
        timestamp inicio
        varchar(45) ip_origen "soporta IPv6"
        varchar(255) user_agent
        boolean exitoso "false en los intentos fallidos"
    }
```

## Relaciones

| Desde | Hacia | Cardinalidad | Clave foranea |
|-------|-------|--------------|---------------|
| `usuarios` | `sesiones` | 1 a N | `sesiones.usuario_id` |

Es la relacion que cumple el requisito de dos tablas relacionadas por base SQL.

## Por que existe `sesiones`

No es relleno. Cada intento de inicio de sesion queda registrado, exitoso o
fallido, con su IP y su navegador. Sirve para detectar intentos de acceso
repetidos contra una misma cuenta, y alimenta la vista analitica de actividad.

## Restricciones

- `usuarios`: `UNIQUE (email)` — no puede haber dos cuentas con el mismo correo.
- `usuarios.rol`: `CHECK` limitado a `ADMIN` o `RESIDENTE`.
- Indices en `usuarios.email` (se busca en cada login) y en
  `sesiones.usuario_id` e `inicio`.

## Sobre `residente_id`

Apunta a la tabla `residentes` de **otra base**, la de `ms-residentes`. No hay
clave foranea: PostgreSQL no puede verificar una referencia fuera de su propia
base. Es un identificador logico, y su validacion es responsabilidad de la
aplicacion, no del motor.

El administrador lo tiene en `NULL`, porque no vive en ninguna unidad.

El DDL completo esta en [schema.sql](schema.sql).
