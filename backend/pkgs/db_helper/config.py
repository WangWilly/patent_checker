from pydantic import Field
from pydantic_settings import BaseSettings

################################################################################

ENV_PREFIX = "DB_"


class Config(BaseSettings, case_sensitive=True):
    host: str = Field(
        alias=ENV_PREFIX + "HOST",
        description="Database host",
    )
    port: int = Field(
        alias=ENV_PREFIX + "PORT",
        description="Database port",
    )
    name: str = Field(
        alias=ENV_PREFIX + "NAME",
        description="Database name",
    )
    user: str = Field(
        alias=ENV_PREFIX + "USER",
        description="Database user",
    )
    password: str = Field(
        alias=ENV_PREFIX + "PASSWORD",
        description="Database password",
    )


################################################################################

if __name__ == "__main__":
    config = Config()
    print(config.model_dump())
