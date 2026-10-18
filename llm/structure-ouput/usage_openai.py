from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


class Product(BaseModel):
    product: str
    price: float
    in_stock: bool


response = client.beta.chat.completions.parse(
    model="gpt-5-mini",
    messages=[
        {"role": "system", "content": "Extract product information"},
        {"role": "user", "content": "Mac Air M4, $500, in stock"},
    ],
    response_format=Product,
)

product = response.choices[0].message.parsed
print(product.product, product.price, product.in_stock)
