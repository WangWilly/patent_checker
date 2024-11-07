from pkgs.errors import RecordNotFoundError

docs_router = {
    "tags": ["infringement"],
}

docs_create_v1 = {
    "summary": "Create assess infringement",
    "description": """
        Create assess infringement record.
    """,
    "responses": {
        500: {"model": RecordNotFoundError.model},
    },
}

docs_get_v1 = {
    "summary": "Get assess infringement",
    "description": """
        Get assess infringement record.
    """,
    "responses": {
        404: {"model": RecordNotFoundError.model},
    },
}
