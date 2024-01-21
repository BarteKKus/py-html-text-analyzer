from pydantic import BaseModel, ValidationError
from pathlib import Path
from typing import List, Dict, Callable
from configuration.json_file_loader import load_json_file


class UrlConfiguration(BaseModel):
    """Represents single url config"""
    id: str
    url: str


def load_urls_configuration(
        filepath: Path,
        loader: Callable[[Path], Dict] = load_json_file
) -> List[UrlConfiguration]:
    """Load file with url(s) to retrieve with theirs identifiers

    Args:
        filepath (FilePath): path with filename to load
        loader (Callable[[FilePath], Dict], optional): file loader. 
            Defaults to load_json_file.

    Returns:
        List[UrlConfiguration]: list with all urls with theirs names
    """
    loaded_configuration = loader(filepath=filepath)

    if 'urls' not in loaded_configuration:
        raise RuntimeError("'urls' key is not present in configuration file!")

    urls_data = loaded_configuration.get('urls')
    try:
        url_list = [UrlConfiguration(**url) for url in urls_data]
    except (ValidationError, TypeError):
        raise RuntimeError(
            f"Cannot create configuration element for {filepath}! "
            "Check configuration file keys corectness with overall strucutre!"
        )
    return url_list
