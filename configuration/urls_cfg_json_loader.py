from dataclasses import dataclass
from pathlib import Path
from typing import List, Callable, Dict
from configuration.json_file_loader import load_json_file

_JSON_KEYS_MAP = {
    'urls': 'urls',
    "name": "id",
    "link": "url"
}


@dataclass
class UrlConfiguration:
    """Represents single url config"""
    name: str
    url: str


def load_urls_configuration(
        filepath: Path,
        loader: Callable[[Path], Dict] = load_json_file
) -> List[UrlConfiguration]:
    """Load file with url(s) to retrieve with theirs identifiers

    Args:
        filepath (Path): path with filename to load
        loader (Callable[[Path], Dict], optional): file loader. 
            Defaults to load_json_file.

    Returns:
        List[UrlConfiguration]: list with all urls with theirs names
    """
    loaded_configuration = loader(filepath=filepath)
    urls = loaded_configuration[_JSON_KEYS_MAP["urls"]]

    return [
        UrlConfiguration(
            name=url[_JSON_KEYS_MAP["name"]],
            url=url[_JSON_KEYS_MAP["link"]]
        )
        for url in urls
    ]
