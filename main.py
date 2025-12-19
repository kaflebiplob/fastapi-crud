from fastapi import FastAPI
from models import Products

app = FastAPI()


@app.get("/")
def greet():
    return "First Fastapi"

products=[
    Products(id=1,name="laptop",description="A high-performance laptop",price=45000.00,quantity=5),
    Products(id=2,name="mobile",description="A smartphone with advanced features",price=25000.00,quantity=10)
]

@app.get("/products")
def get_products():
    return products
@app.get("/product/{id}")
def get_product_by_id(id:int):
    for product in products:
        if product.id == id:
            return product
    return {"error":"Product not found"}
@app.post("/product")
def add_product(product:Products):
    products.append(product)
    return product
    
    