import os

from pydantic import Field
from pydantic_settings import BaseSettings

################################################################################
# Constants

this_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_COMPANY_PRODUCTS_PATH = os.path.join(
    this_dir, "../../assets/company_products.json"
)
DEFAULT_PATENTS_PATH = os.path.join(this_dir, "../../assets/patents.json")

################################################################################

ENV_PREFIX = "PT_GPT_CTRL_"


class Config(BaseSettings, case_sensitive=True):
    company_products_path: str = Field(
        alias=ENV_PREFIX + "COMPANY_PRODUCTS_PATH",
        default=DEFAULT_COMPANY_PRODUCTS_PATH,
        description="Path to the company products JSON file",
    )
    patents_path: str = Field(
        alias=ENV_PREFIX + "PATENTS_PATH",
        default=DEFAULT_PATENTS_PATH,
        description="Path to the patents JSON file",
    )


################################################################################

if __name__ == "__main__":
    config = Config()
    print(config.model_dump())
