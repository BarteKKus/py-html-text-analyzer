from typing import List, Dict, Callable
from pathlib import Path
from pydantic import ValidationError
from configuration.json_file_loader import load_json_file
from configuration.data_structures import (
    SinglePluginData,
    TextConverterPluginFields as Fields,
    ConversionStep
)
from text_conversion_plugins.interfaces import \
    PluginConfigurationInstruction


def load_plugins_configuration(
        file_path: Path,
        configuration_types: Dict[str, PluginConfigurationInstruction],
        loader: Callable[[Path], Dict] = load_json_file,
        configuration_header_key: str = Fields.CONVERSION_STEPS
) -> List[ConversionStep]:
    """Load plugins configuration.

    Args:
        file_path (Path): file path to configuration 
            file that contains plugins description
        configuration_types (Dict[str, PluginConfigurationInstruction]): 
            registered cfg types
        loader (Callable[[Path], Dict], optional): file loader.
            Defaults to load_json_file.
        configuration_header_key (str, optional): Expected most-top file key. 
            Defaults to Fields.CONVERSION_STEPS.

    Raises:
        ValueError: raised on any issue with reading configuration

    Returns:
        List[ConversionStep]: List of loaded conversion steps
    """
    loaded_configuration: Dict = loader(file_path=file_path)
    try:
        return [
            ConversionStep(
                step_name=plugin_name,
                step_instructions=SinglePluginData(
                    **config,
                    configuration_type_key=Fields.CONFIGURATION_TYPE,
                    configuration_key=Fields.CONFIGURATION,
                    configuration_types=configuration_types,
                )
            )
            for plugin_name, config in loaded_configuration.get(
                configuration_header_key
            ).items()
        ]
    except (ValidationError, ValueError, KeyError, TypeError, AttributeError) as er:
        raise ValueError(
            f"Error while loading plugin configuration for {file_path} "
            f"as: '{repr(er)}'"
        )
