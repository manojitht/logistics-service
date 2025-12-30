from fastapi import FastAPI
from app.routers import products
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Logistics Microservice",
    description="A simplified Inventory & Order Management Service",
    version="1.0.0"
)

app.include_router(products.router)

@app.get("/")
def read_root():
    return {"message": "Logistics Service is running. Visit /docs for Swagger UI."}