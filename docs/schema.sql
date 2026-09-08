-- ============================================================
-- ms-usuarios | Esquema inicial (PostgreSQL 16)
-- ============================================================
-- Base propia: condominio_usuarios
--
-- `residente_id` NO es clave foranea: apunta a un registro de la base de
-- ms-residentes, que es otro microservicio con su propia base. Se guarda como
-- identificador logico, igual que hacen ms-pagos y ms-incidencias.
-- ============================================================

-- CREATE DATABASE condominio_usuarios;
-- \c condominio_usuarios

CREATE TABLE IF NOT EXISTS usuarios (
    id             BIGSERIAL PRIMARY KEY,
    -- NULL para el administrador, que no esta ligado a ningun residente.
    residente_id   BIGINT,
    email          VARCHAR(160) NOT NULL,
    password_hash  VARCHAR(255) NOT NULL,   -- bcrypt; NUNCA la password en claro
    rol            VARCHAR(20)  NOT NULL DEFAULT 'RESIDENTE',
    activo         BOOLEAN      NOT NULL DEFAULT TRUE,
    ultimo_login   TIMESTAMP,
    creado_en      TIMESTAMP    NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_usuarios_email UNIQUE (email),
    CONSTRAINT ck_usuarios_rol CHECK (rol IN ('ADMIN', 'RESIDENTE'))
);

CREATE INDEX IF NOT EXISTS idx_usuarios_residente ON usuarios(residente_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_email     ON usuarios(email);

-- ------------------------------------------------------------
-- Tabla: sesiones
-- Registro de los inicios de sesion. Relacionada con usuarios, para cumplir
-- el requisito del curso de al menos 2 tablas relacionadas en una BD SQL.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sesiones (
    id           BIGSERIAL PRIMARY KEY,
    usuario_id   BIGINT       NOT NULL,
    inicio       TIMESTAMP    NOT NULL DEFAULT NOW(),
    ip_origen    VARCHAR(45),             -- soporta IPv6
    user_agent   VARCHAR(255),
    exitoso      BOOLEAN      NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_sesiones_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS idx_sesiones_usuario ON sesiones(usuario_id);
CREATE INDEX IF NOT EXISTS idx_sesiones_inicio  ON sesiones(inicio);
