'''
Seed the database with initial data for development.
'''
import asyncio
import random
import sys
import os
from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import uuid4

import asyncpg
from faker import Faker

# --- Path Hack to fix ModuleNotFoundError ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
# ------------------------------------------

from app.core.config import settings
from app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from app.cuotas.domain.entities import Cuota, TemporadaCuota, TipoCuota
from app.cuotas.domain.value_objects import EstadoPago, MetodoPago, NombreTipoCuota
from app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
from app.cuotas.infrastructure.postgres_temporada_cuota_repository import PostgresTemporadaCuotaRepository
from app.cuotas.infrastructure.postgres_tipo_cuota_repository import PostgresTipoCuotaRepository
from app.infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.domain.entities import User
from app.users.domain.value_objects import Rol
from app.users.infrastructure.postgres_user_repository import PostgresUserRepository
from app.prendas.domain.entities import Prenda, VariantePrenda
from app.prendas.domain.value_objects import TallaPrenda, GeneroPrenda
from app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from app.prendas.application.repositories.i_variante_prenda_repository import IVariantePrendaRepository
from app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository
from app.prendas.infrastructure.postgres_variante_prenda_repository import PostgresVariantePrendaRepository

# --- Configuration ---
NUM_USERS_TO_CREATE = 15
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "Admin123!"
DEFAULT_USER_PASSWORD = "User123!"

async def seed_data():
    '''Main function to seed the database.'''
    print("--- Starting database seeding ---")
    
    pool = None
    db_connection = None
    faker = Faker('es_ES')
    password_hasher = Argon2PasswordHasher()

    try:
        # Manually create a connection pool and acquire a connection
        pool = await asyncpg.create_pool(str(settings.DATABASE_URL))
        db_connection = await pool.acquire()

        # Instantiate repositories
        user_repo: IUserRepository = PostgresUserRepository(db_connection)
        temporada_repo: ITemporadaCuotaRepository = PostgresTemporadaCuotaRepository(db_connection)
        tipo_cuota_repo: ITipoCuotaRepository = PostgresTipoCuotaRepository(db_connection)
        cuota_repo: ICuotaRepository = PostgresCuotaRepository(db_connection)
        prenda_repo: IPrendaRepository = PostgresPrendaRepository(db_connection)
        variante_prenda_repo: IVariantePrendaRepository = PostgresVariantePrendaRepository(db_connection)

        # === 1. Create Users ===
        print(f"Creating {NUM_USERS_TO_CREATE} users and 1 admin...")
        created_users = []

        # Admin user
        admin_user = User(
            id=uuid4(),
            email=ADMIN_EMAIL,
            contrasena_hasheada=password_hasher.hash(ADMIN_PASSWORD),
            nombre="Admin",
            apellidos="User",
            numero_telefono=faker.phone_number(),
            rol=Rol.ADMIN,
            esta_activo=True,
            email_verificado=True,
            aprobado_por_admin=True,
            fecha_creacion=datetime.now(timezone.utc),
            fecha_actualizacion=datetime.now(timezone.utc)
        )
        await user_repo.crear(admin_user)
        created_users.append(admin_user)
        print(f"- Admin user created: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")

        # Regular users
        for i in range(NUM_USERS_TO_CREATE):
            user = User(
                id=uuid4(),
                email=faker.unique.email(),
                contrasena_hasheada=password_hasher.hash(DEFAULT_USER_PASSWORD),
                nombre=faker.first_name(),
                apellidos=faker.last_name(),
                numero_telefono=faker.unique.phone_number(),
                rol=Rol.USUARIO,
                esta_activo=True,
                email_verificado=True,
                aprobado_por_admin=True,
                fecha_creacion=datetime.now(timezone.utc),
                fecha_actualizacion=datetime.now(timezone.utc)
            )
            await user_repo.crear(user)
            created_users.append(user)
        print(f"- {NUM_USERS_TO_CREATE} regular users created with default password: {DEFAULT_USER_PASSWORD}")

        # === 2. Create Seasons and Fee Types ===
        print("Creating seasons and fee types...")
        fee_types_by_season = {}

        # Past Season
        temporada_24_25 = TemporadaCuota(
            id=20242025, # Using a predictable ID
            nombre_temporada="Temporada 2024-2025",
            fecha_inicio=date(2024, 8, 15),
            fecha_fin=date(2025, 8, 14),
            fecha_creacion=datetime.now(timezone.utc)
        )
        await temporada_repo.guardar_temporada(temporada_24_25)

        # Current Season
        temporada_25_26 = TemporadaCuota(
            id=20252026,
            nombre_temporada="Temporada 2025-2026",
            fecha_inicio=date(2025, 8, 15),
            fecha_fin=date(2026, 8, 14),
            fecha_creacion=datetime.now(timezone.utc)
        )
        await temporada_repo.guardar_temporada(temporada_25_26)
        print("- Created seasons: 2024-2025 and 2025-2026")

        # Fee Types for both seasons
        for temporada in [temporada_24_25, temporada_25_26]:
            fee_types_by_season[temporada.id] = []
            alta = TipoCuota(
                id=int(f"{temporada.id}1"), # Predictable ID
                temporada_id=temporada.id,
                nombre=NombreTipoCuota.ALTA, # Use Enum
                importe=Decimal("25.00"),
                fecha_creacion=datetime.now(timezone.utc)
            )
            anual = TipoCuota(
                id=int(f"{temporada.id}2"), # Predictable ID
                temporada_id=temporada.id,
                nombre=NombreTipoCuota.SOCIO, # Use Enum
                importe=Decimal("25.00"),
                fecha_creacion=datetime.now(timezone.utc)
            )
            created_types = await tipo_cuota_repo.guardar_varios([alta, anual])
            fee_types_by_season[temporada.id].extend(created_types)
        print("- Created 'CUOTA DE ALTA' and 'CUOTA ANUAL' for each season.")

        # === 3. Create Fees ===
        print("Creating fees for users...")
        # All users have paid the fee for the past season
        for user in created_users:
            past_season_fee_type = fee_types_by_season[temporada_24_25.id][1] # CUOTA ANUAL
            cuota = Cuota(
                id=uuid4(),
                usuario_id=user.id,
                tipo_de_cuota_id=past_season_fee_type.id,
                importe_pagado=past_season_fee_type.importe,
                estado_pago=EstadoPago.COMPLETADO,
                fecha_pago=faker.date_time_between(start_date=temporada_24_25.fecha_inicio, end_date=temporada_24_25.fecha_fin),
                metodo_pago=random.choice(list(MetodoPago))
            )
            await cuota_repo.guardar(cuota)
        print(f"- All {len(created_users)} users have a completed fee for the 2024-2025 season.")

        # Some users have fees for the current season
        for user in random.sample(created_users, k=int(len(created_users) * 0.8)):
            current_season_fee_type = fee_types_by_season[temporada_25_26.id][1] # CUOTA ANUAL
            estado = random.choice([EstadoPago.PENDIENTE, EstadoPago.COMPLETADO])
            cuota = Cuota(
                id=uuid4(),
                usuario_id=user.id,
                tipo_de_cuota_id=current_season_fee_type.id,
                importe_pagado=current_season_fee_type.importe if estado == EstadoPago.COMPLETADO else Decimal("0.00"),
                estado_pago=estado,
                fecha_pago=datetime.now(timezone.utc) if estado == EstadoPago.COMPLETADO else None,
                metodo_pago=random.choice(list(MetodoPago)) if estado == EstadoPago.COMPLETADO else None
            )
            await cuota_repo.guardar(cuota)
        print("- Approx 80% of users have a fee for the current 2025-2026 season.")

        # === 4. Create Prendas and Variantes ===
        print("Creating prendas and variantes...")
        prendas_data = [
            {"nombre": "Camiseta Técnica", "descripcion": "Camiseta transpirable para entrenamientos.", "precio": "15.00", "imagen_url": "https://via.placeholder.com/150"},
            {"nombre": "Sudadera con Capucha", "descripcion": "Sudadera de algodón con el logo del club.", "precio": "35.50", "imagen_url": "https://via.placeholder.com/150"},
            {"nombre": "Pantalón Corto", "descripcion": "Pantalón corto ideal para correr.", "precio": "20.00", "imagen_url": "https://via.placeholder.com/150"},
        ]
        created_prendas = []
        for prenda_data in prendas_data:
            prenda = Prenda(
                id=uuid4(),
                nombre=prenda_data["nombre"],
                descripcion=prenda_data["descripcion"],
                precio=Decimal(prenda_data["precio"]),
                imagen_url=prenda_data["imagen_url"],
                fecha_creacion=datetime.now(timezone.utc)
            )
            await prenda_repo.guardar(prenda)
            created_prendas.append(prenda)

            # Crear variantes para cada prenda
            for genero in [GeneroPrenda.HOMBRE, GeneroPrenda.MUJER]:
                for talla in [TallaPrenda.S, TallaPrenda.M, TallaPrenda.L]:
                    variante = VariantePrenda(
                        id=uuid4(),
                        prenda_id=prenda.id,
                        genero=genero,
                        talla=talla,
                        fecha_creacion=datetime.now(timezone.utc)
                    )
                    await variante_prenda_repo.guardar(variante)
        print(f"- Created {len(created_prendas)} prendas with their variantes.")

        # === 5. Test Trigger ===
        print("--- Testing database trigger ---")
        user_to_test = created_users[5] # Pick a user who already has a fee
        # This user already has a 'CUOTA ANUAL' for temporada_24_25
        # Let's try to add a 'CUOTA DE ALTA' for the same season. This should fail.
        conflicting_fee_type = fee_types_by_season[temporada_24_25.id][0] # CUOTA DE ALTA
        
        conflicting_cuota = Cuota(
            id=uuid4(),
            usuario_id=user_to_test.id,
            tipo_de_cuota_id=conflicting_fee_type.id,
            importe_pagado=Decimal("0.00"),
            estado_pago=EstadoPago.PENDIENTE
        )
        
        try:
            await cuota_repo.guardar(conflicting_cuota)
            # If this line is reached, the trigger failed
            print("!!! TRIGGER TEST FAILED: A second fee was created for the same user in the same season.")
        except Exception as e:
            # We expect an exception from the database
            if "El usuario ya tiene una cuota asignada para esta temporada" in str(e):
                print("+++ TRIGGER TEST PASSED: The database correctly prevented the creation of a duplicate fee.")
            else:
                print(f"!!! TRIGGER TEST FAILED WITH AN UNEXPECTED ERROR: {e}")

    finally:
        # Ensure the connection and pool are closed
        if db_connection:
            await pool.release(db_connection)
        if pool:
            await pool.close()
        print("--- Database seeding finished ---")

if __name__ == "__main__":
    asyncio.run(seed_data())
