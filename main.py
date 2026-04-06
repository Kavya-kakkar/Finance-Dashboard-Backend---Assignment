from fastapi import FastAPI
from core.database import engine, Base
from routes import auth, users, records, dashboard
from core.config import settings

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Finance Dashboard with strict Role-based access control.",
    version="1.0.0"
)

# Setup routing
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(records.router, prefix="/api/records", tags=["Records"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {"message": "Welcome to the Finance Dashboard API. Visit /docs for Swagger UI documentation."}
