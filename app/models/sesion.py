"""Tabla `sesiones`: historial de intentos de inicio de sesion.

Relacionada con `usuarios` por clave foranea. Registra tanto los logins
exitosos como los fallidos, que sirve para detectar intentos de acceso.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Sesion(Base):
    __tablename__ = "sesiones"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    inicio: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    ip_origen: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(String(255))
    exitoso: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="sesiones")
