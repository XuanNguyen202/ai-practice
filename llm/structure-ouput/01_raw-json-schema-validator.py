


def validate_schema(data, schema):
    errors = []
    _validate(data, schema, "", errors)
    return errors

def _validate(data, schema, path, errors):
    schema_type = schema.get("type")
    if schema_type == "object":
        if not isinstance(data, dict):
            errors.append(f"{path}: expected object, got {type(data).__name__}")
            return
        for key in schema.get("required", []):
            if key not in data:
                errors.append(f"{path}.{key}: missing required field")
        properties = schema.get("properties", {})
        for key, value in data.items():
            if key in properties:
                _validate(value, properties[key], path=f"{path}.{key}", errors=errors)
    elif schema_type == "array":   
        if not isinstance(data, list):
            errors.append(f"{path}: expected array, got {type(data).__name__}")   
            return
        min_items = schema.get("minItems", 0)
        max_items = schema.get("maxItems", float("inf"))
        if len(data) < min_items:
            errors.append(f"{path}: expected at least {min_items} items, got {len(data)}")
        if len(data) > max_items:
            errors.append(f"{path}: expected at most {max_items} items, got {len(data)}")
        item_schema = schema.get("items")
        for i, item in enumerate(data):
            _validate(item, item_schema, f"{path}[{i}]", errors)

    elif schema_type == "string":
        if not isinstance(data, str):
            errors.append(f"{path}: expected string, got {type(data).__name__}")
            return
        enum_values = schema.get("enum")
        if enum_values and data not in enum_values:
            errors.append(f"{path}: '{data}' not in allowed values {enum_values}")

    elif schema_type == "number":
        if not isinstance(data, (int, float)) or isinstance(data, bool):
            errors.append(f"{path}: expected number, got {type(data).__name__}")
            return
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if minimum is not None and data < minimum:
            errors.append(f"{path}: {data} is less than minimum {minimum}")
        if maximum is not None and data > maximum:
            errors.append(f"{path}: {data} is greater than maximum {maximum}")

    elif schema_type == "boolean":
        if not isinstance(data, bool):
            errors.append(f"{path}: expected boolean, got {type(data).__name__}")
            return

    elif schema_type == "integer":
        if not isinstance(data, int) or isinstance(data, bool):
            errors.append(f"{path}: expected integer, got {type(data).__name__}")

if __name__ == "__main__":
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0, "maximum": 120},
            "score": {"type": "number", "minimum": 0, "maximum": 100},
            "role": {"type": "string", "enum": ["student", "teacher"]},
            "tags": {
                "type": "array",
                "minItems": 1,
                "maxItems": 3,
                "items": {"type": "string"},
            },
            "active": {"type": "boolean"},
        },
        "required": ["name", "age", "score", "role", "active"],
    }

    valid_data = {
        "name": "Linh",
        "age": 20,
        "score": 95.5,
        "role": "student",
        "tags": ["python", "ai"],
        "active": True,
    }
    assert validate_schema(valid_data, schema) == []

    invalid_data = {
        "name": 10,
        "age": True,
        "score": 120,
        "role": "admin",
        "tags": ["python", 5, "ai", "extra"],
        "active": 1,
    }
    errors = validate_schema(invalid_data, schema)
    assert len(errors) == 7, errors
    assert any("age: expected integer" in error for error in errors)
    assert any("score: 120 is greater than maximum 100" in error for error in errors)
    assert any("role: 'admin' not in allowed values" in error for error in errors)

    missing_required_data = {}
    errors = validate_schema(missing_required_data, schema)
    assert len(errors) == 5, errors
    assert any("name: missing required field" in error for error in errors)

    print("All tests passed: valid data, invalid values, and required fields.")
