from pkgs.errors import GptNotWorkingError, RecordNotFoundError

docs_router = {
    "tags": ["gpt"],
}

docs_assess_infringement_v1 = {
    "summary": "Assess infringement by using GPT",
    "description": """
        Only apply to the stored patents and companies. If the patent or company is not found, it will return 404.
        204 is returned if no infringement is found.
    """,
    "responses": {
        204: {},
        404: {"model": RecordNotFoundError.model},
        500: {"model": GptNotWorkingError.model},
    },
}
