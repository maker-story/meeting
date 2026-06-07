from fastapi import FastAPI
from infrastructure.database import Base, engine
from presentation.router.user_router import router as user_router
from infrastructure.provider.user_provider import register_user_di


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Meeting Project Management System",
    description="Clean Architecture implementation with FastAPI",
    version="1.0.0"
)

app.include_router(user_router)
register_user_di(app)