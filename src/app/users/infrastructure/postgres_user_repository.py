from typing import List, Optional
from uuid import UUID
import asyncpg
from datetime import datetime, timezone

from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.domain.entities import User
from app.users.domain.value_objects import Rol


class PostgresUserRepository(IUserRepository):
    def __init__(self, db_connection: asyncpg.Connection):
        self.db_connection = db_connection

    async def crear(self, user: User) -> User:
        query = """
        INSERT INTO usuarios (id, email, contrasena_hasheada, nombre, apellidos, numero_telefono, rol, apodo, url_avatar, esta_activo, email_verificado, aprobado_por_admin, fecha_creacion, fecha_actualizacion)
        VALUES ($1, $2, $3, $4, $5, $6, $7::rol, $8, $9, $10, $11, $12, $13, $14)
        """
        await self.db_connection.execute(
            query,
            user.id,
            user.email,
            user.contrasena_hasheada,
            user.nombre,
            user.apellidos,
            user.numero_telefono,
            user.rol.value,
            user.apodo,
            user.url_avatar,
            user.esta_activo,
            user.email_verificado,
            user.aprobado_por_admin,
            user.fecha_creacion,
            user.fecha_actualizacion
        )
        return user

    async def buscar_por_email(self, email: str) -> Optional[User]:
        query = "SELECT * FROM usuarios WHERE email = $1"
        row = await self.db_connection.fetchrow(query, email)
        if row:
            return User(
                id=row['id'],
                email=row['email'],
                contrasena_hasheada=row['contrasena_hasheada'],
                nombre=row['nombre'],
                apellidos=row['apellidos'],
                numero_telefono=row['numero_telefono'],
                rol=Rol(row['rol']),
                apodo=row['apodo'],
                url_avatar=row['url_avatar'],
                esta_activo=row['esta_activo'],
                email_verificado=row['email_verificado'],
                aprobado_por_admin=row['aprobado_por_admin'],
                fecha_creacion=row['fecha_creacion'],
                fecha_actualizacion=row['fecha_actualizacion']
            )
        return None

    async def buscar_por_id(self, user_id: UUID) -> Optional[User]:
        query = "SELECT * FROM usuarios WHERE id = $1"
        row = await self.db_connection.fetchrow(query, user_id)
        if row:
            return User(
                id=row['id'],
                email=row['email'],
                contrasena_hasheada=row['contrasena_hasheada'],
                nombre=row['nombre'],
                apellidos=row['apellidos'],
                numero_telefono=row['numero_telefono'],
                rol=Rol(row['rol']),
                apodo=row['apodo'],
                url_avatar=row['url_avatar'],
                esta_activo=row['esta_activo'],
                email_verificado=row['email_verificado'],
                aprobado_por_admin=row['aprobado_por_admin'],
                fecha_creacion=row['fecha_creacion'],
                fecha_actualizacion=row['fecha_actualizacion']
            )
        return None

    async def actualizar(self, user: User) -> User:
        query = """
        UPDATE usuarios
        SET nombre = $2, apellidos = $3, numero_telefono = $4, apodo = $5, url_avatar = $6, rol = $7::rol, esta_activo = $8, email_verificado = $9, aprobado_por_admin = $10, fecha_actualizacion = $11
        WHERE id = $1
        """
        await self.db_connection.execute(
            query,
            user.id,
            user.nombre,
            user.apellidos,
            user.numero_telefono,
            user.apodo,
            user.url_avatar,
            user.rol.value,
            user.esta_activo,
            user.email_verificado,
            user.aprobado_por_admin,
            user.fecha_actualizacion
        )
        return user

    async def actualizar_contrasena(self, user_id: UUID, contrasena_hasheada: str) -> None:
        query = """
        UPDATE usuarios
        SET contrasena_hasheada = $2, fecha_actualizacion = $3
        WHERE id = $1
        """
        await self.db_connection.execute(query, user_id, contrasena_hasheada, datetime.now(timezone.utc))

    async def desactivar_cuenta(self, user_id: UUID) -> None:
        query = """
        UPDATE usuarios
        SET esta_activo = FALSE, fecha_actualizacion = $2
        WHERE id = $1
        """
        await self.db_connection.execute(query, user_id, datetime.now(timezone.utc))

    async def buscar_todos(self) -> List[User]:
        query = "SELECT * FROM usuarios"
        rows = await self.db_connection.fetch(query)
        return [User(
            id=row['id'],
            email=row['email'],
            contrasena_hasheada=row['contrasena_hasheada'],
            nombre=row['nombre'],
            apellidos=row['apellidos'],
            numero_telefono=row['numero_telefono'],
            rol=Rol(row['rol']),
            apodo=row['apodo'],
            url_avatar=row['url_avatar'],
            esta_activo=row['esta_activo'],
            email_verificado=row['email_verificado'],
            aprobado_por_admin=row['aprobado_por_admin'],
            fecha_creacion=row['fecha_creacion'],
            fecha_actualizacion=row['fecha_actualizacion']
        ) for row in rows]

    async def eliminar_por_id(self, user_id: UUID) -> None:
        query = "DELETE FROM usuarios WHERE id = $1"
        await self.db_connection.execute(query, user_id)

    async def desactivar_usuarios(self, user_ids: List[UUID]) -> None:
        if not user_ids:
            return
        # Convert UUIDs to string for the IN clause
        user_ids_str = [str(uid) for uid in user_ids]
        # Using UNNEST for a more efficient way to pass a list of UUIDs
        query = """
        UPDATE usuarios
        SET esta_activo = FALSE, fecha_actualizacion = $1
        WHERE id = ANY($2::uuid[])
        """
        await self.db_connection.execute(query, datetime.now(timezone.utc), user_ids_str)
