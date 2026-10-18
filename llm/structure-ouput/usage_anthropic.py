import anthropic

client = anthropic.Anthropic()

response = client.message.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[
        {
            "name": "extract_product",
            "description": "Extract product information from text",
            "input_schema": {
                "type": "object",
                "properties": {
                    "product": {"type": "string"},
                    "price": {"type": "number"},
                    "in_stock": {"type": "boolean"},
                },
                "required": ["product", "price", "in_stock"],
            },
        }
    ],
    messages=[{"role": "user", "content": "Extract: Macbook Air M4, $547, in stock"}],
)
