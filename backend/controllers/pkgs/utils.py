import json
import os

from pkgs.dto.companies import Companies
from pkgs.dto.patent import Patents

################################################################################


def load_companies(path: str) -> Companies:
    if not os.path.exists(path):
        return Companies()

    json_data = None
    with open(path, "r") as f:
        json_data = json.load(f)

    return Companies.from_dict(json_data["companies"])


def load_patents(path: str) -> Patents:
    if not os.path.exists(path):
        return Patents()

    json_data = None
    with open(path, "r") as f:
        json_data = json.load(f)

    return Patents.from_dict(json_data)
