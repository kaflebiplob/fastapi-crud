from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Products
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "First Fastapi"


products = [
    Products(
        id=1,
        name="laptop",
        description="A high-performance laptop",
        price=45000.00,
        quantity=5,
    ),
    Products(
        id=2,
        name="mobile",
        description="A smartphone with advanced features",
        price=25000.00,
        quantity=10,
    ),
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = SessionLocal()

    count = db.query(database_models.Products).count()
    if count == 0:
        for product in products:
            db.add(database_models.Products(**product.model_dump()))
        db.commit()


init_db()


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    # db = Sessio nLocal()
    # db.query()
    return db.query(database_models.Products).all()


@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = (
        db.query(database_models.Products)
        .filter(database_models.Products.id == id)
        .first()
    )
    if product:
        return product
    return {"error": "Product not found"}


@app.post("/products")
def add_product(product: Products, db: Session = Depends(get_db)):
    db.add(database_models.Products(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id: int, product: Products, db: Session = Depends(get_db)):
    updated_product = (
        db.query(database_models.Products)
        .filter(database_models.Products.id == id)
        .first()
    )
    if updated_product:
        for key, value in product.model_dump().items():
            setattr(updated_product, key, value)
        db.commit()
        return updated_product
    return {"error": "Product not found"}


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = (
        db.query(database_models.Products)
        .filter(database_models.Products.id == id)
        .first()
    )
    if product:
        db.delete(product)
        db.commit()
        return "Product deleted successfully"
    return "No Product found"
