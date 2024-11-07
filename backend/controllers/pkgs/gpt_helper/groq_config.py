from pydantic import Field
from pydantic_settings import BaseSettings

################################################################################

ENV_PREFIX = "PT_GPT_"


class Config(BaseSettings, case_sensitive=True):
    groq_api_key: str = Field(
        alias=ENV_PREFIX + "GROQ_API_KEY",
        default="",
        description="GROQ API key",
    )


################################################################################

if __name__ == "__main__":
    config = Config()
    print(config.model_dump())
