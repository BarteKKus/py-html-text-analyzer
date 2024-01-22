from pydantic import ValidationError
from pathlib import Path
from typing import Dict, Callable
from configuration.json_file_loader import load_json_file
from configuration.data_structures import SingleUrlSetting, UrlsConfiguration


def load_urls_configuration(
        file_path: Path,
        loader: Callable[[Path], Dict] = load_json_file
) -> UrlsConfiguration:
    """Loads urls configuration.

    Args:
        filepath (Path): file path to configuration file 
            that contains plugins description
        loader (Callable[[Path], Dict], optional): file loader.
            Defaults to load_json_file.

    Raises:
        ValueError: raised on any issue with reading configuration

    Returns:
        UrlsConfiguration: total urls pack
    """
    loaded_configuration = loader(file_path=file_path)
    try:
        config_object = UrlsConfiguration.model_validate(
            loaded_configuration
        )
    except (ValidationError, ValueError, KeyError, TypeError) as e:
        raise ValueError(
            f"Error while loading urls configuration for {file_path} "
            f"as: '{repr(e)}'"
        )
    return config_object
