from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Protocol


class FilesDescriptor(Protocol):

    @property
    def get_files_directory(self) -> Path:
        ...


@dataclass
class JSONUrlFilesDescriptor(FilesDescriptor):
    """Contains description of url configuration json files"""
    correct: List[str] = field(
        default_factory=lambda: ['correct.json']
    )
    incorrect_data: List[str] = field(
        default_factory=lambda: ['invalid_url.json']
    )
    unexpected_key_name: List[str] = field(
        default_factory=lambda: [
            'misspelled_inner_key.json',
            'misspelled_key.json'
        ]
    )
    incorrect_structure: List[str] = field(
        default_factory=lambda: ['wrong_structure.json']
    )
    detailed_evaluation: List[str] = field(
        default_factory=lambda: [
            'correct_to_detailed_evaluation.json'
        ]
    )

    @property
    def get_files_directory(self) -> Path:
        return Path() / 'tests' / 'data' / 'json_url_files'


@dataclass
class JSONPluginFilesDescriptor(FilesDescriptor):
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
            'misspelled_main_key.json'
        ]
    )
    non_existent_resource: List[str] = field(
        default_factory=lambda: [
            'not_existing_plugin.json',
        ]
    )
    detailed_evaluation: List[str] = field(
        default_factory=lambda: [
            'correct_to_detailed_evaluation.json'
        ]
    )

    @property
    def get_files_directory(self) -> Path:
        return Path() / 'tests' / 'data' / 'json_plugins_files'
