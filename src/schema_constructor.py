from typing import Dict

from schema import Schema, Optional


class SchemaConstructor:

    def __init__(self, schema: Schema):
        for key in schema._schema:
            if isinstance(key, Optional):
                setattr(self, key._schema, None)
            else:
                setattr(self, key, None)
