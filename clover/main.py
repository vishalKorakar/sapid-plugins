    from typing import Union
    from fastapi import FastAPI
    import requests
    import uvicorn
    import json
    import os
    import dotenv
    from pydantic import BaseModel
    # import uuid


    # Pydantic models
    class ItemUpdate(BaseModel):
        item_id: str
        item_name: str
        item_price: int

    class SessionCustomer(BaseModel):
        session_uuid: str

    class CreateOrder(BaseModel):
        client_id: str
        item_name: str
        quantity: int

    app = FastAPI(title="Clover API", description="API for Clover")

    # Load environment variables from parent directory
    dotenv.load_dotenv("../.env")
    # session_uuid = str(uuid.uuid4())

    @app.get("/api/getItems")
    def get_items():

        url = f"https://apisandbox.dev.clover.com/v3/merchants/{os.getenv('MERCHANT_ID')}/items"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {os.getenv('TOKEN')}"
        }

        response = requests.get(url, headers=headers)

        return response.json()


    @app.post("/api/createSessionCustomer")
    def create_session_customer(data: SessionCustomer):
        
        HEADERS = {
            "accept": "application/json",
            "authorization": f"Bearer {os.getenv('TOKEN')}",
            "Content-Type": "application/json"
        }

        payload = {
            "externalid": data.session_uuid,
            "firstName": "Client Session: ",
            "lastName": str(data.session_uuid)
        }

        print("📦payload: ", payload)
        print("🔑data: ", data.session_uuid)

        customer_id = get_customer_by_session_uuid(data.session_uuid)
        
        if customer_id:
            print(f"🛃Customer already exists: {customer_id}")
            return customer_id
        else:
            res = requests.post(f"{os.getenv('BASE_URL')}/{os.getenv('MERCHANT_ID')}/customers", headers=HEADERS, json=payload)
            print(f"🆕Customer created: {res.json()}")
            return res.json()


    def get_customer_by_session_uuid(session_uuid):
        # Customer already exists — find it
        HEADERS = {
            "accept": "application/json",
            "authorization": f"Bearer {os.getenv('TOKEN')}",
            "Content-Type": "application/json"
        }

        query = requests.get(f"{os.getenv('BASE_URL')}/{os.getenv('MERCHANT_ID')}/customers", headers=HEADERS)
        customer_id = query.json()

        for customer in customer_id.get("elements", []):
            if customer.get("lastName") == session_uuid:
                return customer.get("id")
        return False


    @app.post("/api/createOrder")
    def create_order(order: CreateOrder):
        payload = {
            "state": "OPEN",
            "customer": { "id": order.client_id },
            "lineItems": [
                {
                    "item": { "id": order.item_name },
                    "unitQty": order.quantity
                }
            ]
        }

        res = requests.post(f"{os.getenv('BASE_URL')}/{os.getenv('MERCHANT_ID')}/orders", headers=HEADERS, json=payload)
        res.raise_for_status()
        return res.json()




    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
