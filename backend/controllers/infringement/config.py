# import os

# from pydantic import Field
from pydantic_settings import BaseSettings

################################################################################
# Constants

# this_dir = os.path.dirname(os.path.abspath(__file__))

################################################################################

ENV_PREFIX = "PT_INFRINGEMENT_CTRL_"


class Config(BaseSettings, case_sensitive=True):
    pass


################################################################################

if __name__ == "__main__":
    config = Config()
    print(config.model_dump())
