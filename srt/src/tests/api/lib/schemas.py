# ~*~ coding: utf-8 ~*~

from jsonschema import validate
from functools import partial

from  src.tests.api.lib.queries import new_token, get_json



DATA = 'data'
MSG_1 = " make_load() - arguments should be dictionaries"
MSG_2 = "There is no such key in this dictionary"

# Return list of dicts
def unpack_r(response):
    return response[DATA]

def unpack_count(request):
    return get_json(request)['count']

def unpack_data(request):
    return get_json(request)['data']

def assert_response(response, schema_name):
    fn = lambda schema_name, part: validate(part, schema_name)
    return map(partial(fn, schema_name), unpack_r(response))

def make_load(data):
    load = new_token()

    if not isinstance(data, dict):
        return ValueError(MSG)

    load.update(data)
    return load



# Responses data structure
# All Json's are made via JSON Schema convention

BRANCH_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
    },
}

EMPLOYEES_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "phone": {"type": "string"},
        "email": {"type": "string"},
        "deleted": {"type": "boolean"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "earnings": {
            "type": "array",
            "properties": {
                "type" : {"type": "number"},
                "value" : {"type": "number"},
            },
        },
    },
}

MARGIN_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "title": {"type": "string"},
        "margin": {"type": "number"},
    },
}

STATUS_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "color": {"type": "string"},
        "name": {"type": "string"},
        "group": {"type": "number"},
    },
}

# Customer schemas
CLIENT_SOURCE_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "title": {"type": "string"},
    },
}

CLIENT_LIST_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "phone": {"type": "array"},
        "email": {"type": "string"},
        # Waiting for bug fix under DEV-993
        "notes": {"type": "string"},
        "address": {"type": "string"},
        "supplier": {"type": "boolean"},
        "juridical": {"type": "boolean"},
        "conflicted": {"type": "boolean"},
        "modified_at": {"type": "number"},
        "marketing_source": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "title": {"type": "string"},
            },
        },
    },
}

NEW_CLIENT_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
    },
}

# Order schemas
ORDER_C_F_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "type": {"type": "number"},
    },
}

ORDER_TYPES_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
    },
}


ORDER_JSON = {
# Waiting for bug fix under DEV-993
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "brand": {"type": "string"},
        "model": {"type": "string"},
        "price": {"type": "number"},
        "payed": {"type": "number"},
        "resume": {"type": "string"},
        "urgent": {"type": "boolean"},
        "serial": {"type": "string"},
        "client": CLIENT_LIST_JSON,
        "status": STATUS_JSON,

        "overdue": {"type": "boolean"},
        "engineer_id": {"type": "number"},
        "manager_id": {"type": "number"},
        "branch_id": {"type": "number"},
        "appearance": {"type": "string"},
        "created_by_id": {"type": "number"},
        "order_type": ORDER_TYPES_JSON,
        "operations": {"type": "array"},
        "parts": {"type": "array"},
        "created_at": {"type": "number"},
        "modified_at": {"type": "number"},
        "packagelist": {"type": "string"},
        "kindof_good": {"type": "string"},
        "malfunction": {"type": "string"},
        "id_label": {"type": "string"},
        "closed_by_id": {"type": "number"},
        "custom_fields": ORDER_C_F_JSON,
        "manager_notes": {"type": "string"},
        "engineer_notes": {"type": "string"},

    # Data is kept as None till it's set as 'number'
    # Since this we are not checking such types of data
        # "estimated_done_at": {"type": "number"},
        # "done_at": {"type": "number"},
        # "assigned_at": {"type": "number"},
        # "closed_at": {"type": "number"},
        # "warranty_date": {"type": "number"},
        # "estimated_cost": {"type": "number"},
    },
}

# Books schemas
MODELS_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "title": {"type": "string"},
    },
}

SERVICES_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "title": {"type": "string"},
        "price": {"type": "number"},
    },
}

# Warehouse schema

STOCK_JSON =  {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "is_global": {"type": "boolean"},
        "title": {"type": "string"},
    },
}

CATEGORIES_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "title": {"type": "string"},
        "parent_id": {"type": ["number", "null"]},
    },
}

GOODS_JSON = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "code": {"type": "string"},
        "title": {"type": "string"},
        "price": MARGIN_JSON,
        "article": {"type": "string"},
        "residue": {"type": "number"},
        "category": CATEGORIES_JSON,
        "description": {"type": "string"},
        "image": {"type": "string"},
    },
}
