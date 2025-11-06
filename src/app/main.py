import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def include_routers():
    from app.users.presentation.router import router as users_router
    from app.cuotas.presentation.router import router as cuotas_router
    from app.prendas.presentation.router import router as prendas_router
    from app.users.presentation.admin_router import router as admin_users_router
    from app.pedidos.presentation.router import router as pedidos_router
    from app.pedidos.presentation.router import router_admin as pedidos_admin_router
    from app.pedidos.presentation.router import router_webhooks as pedidos_webhooks_router

    app.include_router(users_router, prefix=settings.API_V1_STR)
    app.include_router(prendas_router, prefix=settings.API_V1_STR)
    app.include_router(cuotas_router, prefix=settings.API_V1_STR)
    app.include_router(pedidos_router, prefix=settings.API_V1_STR)
    app.include_router(pedidos_webhooks_router, prefix=settings.API_V1_STR) # Añadido

    app.include_router(admin_users_router, prefix=settings.API_V1_STR)
    app.include_router(pedidos_admin_router, prefix=settings.API_V1_STR)

include_routers()
