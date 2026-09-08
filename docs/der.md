# Diagrama Entidad-Relacion - ms-usuarios (PostgreSQL)

> PLACEHOLDER. Reemplazar por el diagrama definitivo (`der.png` / `der.drawio`)
> antes de la primera entrega.

## Entidades

- **usuarios**: cuentas de acceso al sistema (register / login).
- **sesiones**: historial de intentos de inicio de sesion, exitosos y fallidos.

## Relaciones

```
usuarios (1) ──< (N) sesiones
```

- Un usuario acumula muchos intentos de login (`sesiones.usuario_id` -> `usuarios.id`).
- Esta es la relacion que cumple el requisito del curso de minimo 2 tablas
  relacionadas en una base SQL.

## Frontera con ms-residentes

`usuarios.residente_id` **no** es clave foranea: apunta a un registro de la base
de ms-residentes, que es otro microservicio con su propia base. Se guarda como
identificador logico y no se valida por HTTP, igual que hacen ms-pagos y
ms-incidencias.

El administrador tiene `residente_id` nulo porque no vive en ninguna unidad.

## Imagen

<!-- ![Diagrama ER](der.png) -->
