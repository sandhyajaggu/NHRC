import app.models.board_member
from fastapi import FastAPI
from app.db.base import Base
from app.core.database import engine
from app.api.v1 import membership, auth, contact,otp,upload,password_reset,admin
from app.api.v1.auth import router as auth_router
from app.models import user, member_benefit, black_profile
from fastapi.openapi.utils import get_openapi
from app.models.board_member import BoardMember
from fastapi.middleware.cors import CORSMiddleware
from app.models import user, board_member, member_benefit, black_profile
print("DB URL:", engine.url)
Base.metadata.create_all(bind=engine)
print("Tables:", Base.metadata.tables.keys())
app = FastAPI(title="NHRC Backend")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="NHRC API",
        version="1.0.0",
        description="NHRC Backend APIs",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(membership.router)
app.include_router(auth.router)
app.include_router(contact.router)
app.include_router(otp.router)
app.include_router(upload.router)
app.include_router(password_reset.router)
app.include_router(admin.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # later replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





