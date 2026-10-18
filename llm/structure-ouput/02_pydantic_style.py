class SchemaValidate:
    def __init__(
        self,
        field_type,
        required=True,
        default=None,
        enum=None,
        minimum=None,
        maximum=None,
    ):
        self.field_type = field_type
        self.required = required
        self.default = default
        self.enum = enum
        self.minimum = minimum
        self.maximum = maximum


def python_type_to_schema(field):
    type_map = {str: "string", int: "integer", float: "number", bool: "boolean"}

    schema = {}

    if field.field_type in type_map:
        schema["type"] = type_map[field.field_type]
    elif field.field_type == list:
        schema["type"] = "array"
        schema["items"] = {"type": "string"}
    elif isinstance(field.field_type, dict):
        schema = field.field_type

    if field.enum:
        schema["enum"] = field.enum
    if field.minimum is not None:
        schema["minimum"] = field.minimum
    if field.maximum is not None:
        schema["maximum"] = field.maximum

    return schema


def model_to_schema(name, fields):
    properties = {}
    required = []

    for field_name, field in fields.items():
        properties[field_name] = python_type_to_schema(field)
        if field.required:
            required.append(field_name)

    return {
        "type": "object",
        "properties": properties,
        "required": required,
    }


if __name__ == "__main__":
    fields = {
        "name": SchemaValidate(str),
        "age": SchemaValidate(int, minimum=0, maximum=120),
        "role": SchemaValidate(str, enum=["student", "teacher"]),
        "tags": SchemaValidate(list, required=False),
    }

    expected = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0, "maximum": 120},
            "role": {"type": "string", "enum": ["student", "teacher"]},
            "tags": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["name", "age", "role"],
    }

    result = model_to_schema("Person", fields)
    assert result == expected, f"Expected {expected}, got {result}"
    print("Test passed: model_to_schema generated the expected schema.")
