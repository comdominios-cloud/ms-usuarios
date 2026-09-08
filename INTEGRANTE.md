# Integrante responsable

| | |
|---|---|
| **Repositorio** | `ms-usuarios` |
| **Integrante** | [@Osomar1705](https://github.com/Osomar1705) |
| **Rol** | API con base de datos (Python / PostgreSQL) |
| **Puerto** | 9006 publicado, 8000 interno |

## Alcance

`ms-usuarios`: cuentas de acceso al sistema (register, login, alta y baja) sobre
su propia base PostgreSQL `condominio_usuarios`.

> ### Por que existe este repositorio
>
> El ACL confirmo que **usuarios debe ser su propio microservicio, con su base
> de datos correspondiente**. Antes estaba dentro de `ms-residentes`; se separo
> el 2026-09-08.
>
> Es el **unico servicio que emite tokens**. Los demas los verifican localmente
> con el mismo `JWT_SECRET`, sin llamarlo por HTTP.

## Avance del 50% — entrega del 6 al 12 de septiembre

- [x] Base **PostgreSQL** propia (`condominio_usuarios`) con volumen persistente
- [x] Tablas `usuarios` y `sesiones` relacionadas ([docs/schema.sql](docs/schema.sql))
- [x] Datos de prueba cargados
- [x] `POST /auth/register` y `POST /auth/login` funcionando
- [x] CRUD de usuarios protegido por token y rol
- [x] Publicado en el puerto **9006** en local
- [x] **Coleccion de Postman** (11/11 requests verificados)
- [ ] Imagen en **Docker Hub**
- [ ] Corriendo en la VM de produccion, con la base en la VM de base de datos

## Como trabajamos

Cada repositorio pertenece a un integrante y se desarrolla de forma
**independiente**: las APIs con base de datos no se llaman entre si. El unico
punto de contacto de este servicio con los demas es el `JWT_SECRET` compartido,
que les permite verificar los tokens sin pedirle nada.

## Equipo

| Repositorio | Integrante | Rol | Puerto |
|---|---|---|---|
| [ms-residentes](https://github.com/comdominios-cloud/ms-residentes) | @Osomar1705 | API con BD - Python / PostgreSQL | 9001 |
| [ms-pagos](https://github.com/comdominios-cloud/ms-pagos) | @sebastianperez72 | API con BD - Java / MySQL | 9002 |
| [ms-incidencias](https://github.com/comdominios-cloud/ms-incidencias) | @fabianbot1331 | API con BD - lenguaje por definir / MongoDB | 9003 |
| [ms-ficha-residente](https://github.com/comdominios-cloud/ms-ficha-residente) | @Brisseth-raton | Backend / Infraestructura | 9004 |
| [ms-analitico](https://github.com/comdominios-cloud/ms-analitico) | @carloscondor1610 | Data Science | 9005 |
| [ms-usuarios](https://github.com/comdominios-cloud/ms-usuarios) | @Osomar1705 | API con BD - Python / PostgreSQL | 9006 |
| [web-condominio](https://github.com/comdominios-cloud/web-condominio) | @alxgr-08 | Frontend / Amplify | 5173 (dev) |
| [ingesta-datos](https://github.com/comdominios-cloud/ingesta-datos) | @carloscondor1610 | Data Science | — |

> CS2032 Cloud Computing - UTEC | Sistema de Administracion de Condominios
