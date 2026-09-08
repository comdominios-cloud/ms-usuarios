"""Tabla `usuarios`: cuentas de acceso al sistema.

Nunca guarda la password: solo su hash bcrypt.

`residente_id` es un IDENTIFICADOR LOGICO: apunta a un registro que vive en la
base de ms-residentes, otro microservicio. Por eso no hay clave foranea ni
llamada HTTP: cada servicio es autonomo.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    # NULL para el administrador, que no esta ligado a ningun residente.
    residente_id: Mapped[int | None] = mapped_column()
    email: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), nullable=False, default="RESIDENTE")
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    ultimo_login: Mapped[datetime | None] = mapped_column(DateTime)
    creado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Un usuario tiene muchos intentos de inicio de sesion.
    sesiones: Mapped[list["Sesion"]] = relationship(back_populates="usuario")
