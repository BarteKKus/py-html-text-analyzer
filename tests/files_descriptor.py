from dataclasses import dataclass, field
from typing import List


@dataclass
class JSONPluginFilesDescriptor:
    """Contains description of plugin configuration json files"""
    correct: List[str] = field(
        default_factory=lambda: ['correct.json']
    )
    incorrect_file_format: List[str] = field(
        default_factory=lambda: ['missing_bracket.json']
    )
    unexpected_key_name: List[str] = field(
        default_factory=lambda: [
            'misspelled_configuration_key.json',
            'misspelled_key.json',
        ]
    )
    non_existent_resource: List[str] = field(
        default_factory=lambda: [
            'not_existing_plugin.json',
        ]
    )
