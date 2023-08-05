"""Collection of utils."""
import pathlib
from typing import Any, MutableMapping, Union

import toml
import yaml


def read_adfh_file(file: str) -> Union[MutableMapping[str, Any], str]:
    """Parse an ADFH file into dict.

    Args:
        file: Path to ADFH file.

    Returns:
        Tuple either with the data or an error message.
    """
    file_path = pathlib.Path(file)
    file_name, file_extension = file_path.name.rsplit(".")

    if file_path.exists() and file_path.is_file():

        if file_extension in ["yaml", "yml"]:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
            return data

        elif file_extension == "toml":
            data = toml.load(f"{file_path}")
            return data
        else:
            return "You can only pick toml or yaml file."
    else:
        return "File doesn't exist."
