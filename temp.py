from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import run


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item

if __name__ == "__main__":
    run(app=app, host="127.0.0.1", port=80)