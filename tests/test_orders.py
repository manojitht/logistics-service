from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order_success():
    # creatiung a product first
    product_res = client.post("/products/", json={"name": "Test Phone", "price": 1000.0, "stock_quantity": 10})
    product_id = product_res.json()["id"]
    
    # placing order for 2 in quantity
    order_res = client.post("/orders/", json={
        "items": [{"product_id": product_id, "quantity": 2}]
    })
    
    # order placing
    assert order_res.status_code == 200
    data = order_res.json()
    assert data["status"] == "Pending"
    assert data["items"][0]["quantity_ordered"] == 2

def test_create_order_insufficient_stock():
    # creating a product with 1 itmem in stock
    product_res = client.post("/products/", json={"name": "Rare Item", "price": 500.0, "stock_quantity": 1})
    product_id = product_res.json()["id"]
    
    # 2. but I'm trying to put 5 in order and it should fail
    order_res = client.post("/orders/", json={
        "items": [{"product_id": product_id, "quantity": 5}]
    })
    
    # 3.verifying the stat code as 400 for insufficient stock
    assert order_res.status_code == 400
    assert "Insufficient stock" in order_res.json()["detail"]

