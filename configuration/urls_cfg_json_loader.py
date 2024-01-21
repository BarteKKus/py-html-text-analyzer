from pydantic import BaseModel
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

    urls_data = loaded_configuration.get('urls', [])

    if not isinstance(urls_data, list):
        raise ValueError("Urls data is not in the expected format!")

    url_list = [UrlConfiguration(**url) for url in urls_data]
    return url_list
