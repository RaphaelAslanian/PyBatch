from typing import Dict, Any

from schema import Schema, Optional


class SchemaConstructor:

    def __init__(self, schema: Schema, default_values: Dict, defined_values: Dict):
        # Fill values
        for key in schema._schema:
            if isinstance(key, Optional):
                setattr(self, key._schema, None)
            else:
                setattr(self, key, None)
        # Fill default values
        for key, val in default_values.items():
            setattr(self, key, val)
        for key, val in defined_values.items():
            setattr(self, key, val)
