from typing import List
from pydantic import BaseModel, ConfigDict, model_validator
from text_conversion_plugins.interfaces import PluginConfigurationInstruction

# PLUGINS SECTION:


class TextConverterPluginFields:
    """Represents map between in-code references to json expected keys"""
    CONVERSION_STEPS: str = 'conversion_steps'
    PLUGIN: str = 'plugin'
    CONFIGURATION_TYPE: str = 'configuration_type'
    CONFIGURATION: str = 'configuration'


class SinglePluginData(BaseModel):
    """Represents single plugin data structure"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    plugin: str
    configuration_type: str
    configuration: List[PluginConfigurationInstruction]

    @model_validator(mode='before')
    def initialize_configuration_field_for_type(
        cls,
        values,
    ):
        configuration_types = values.get('configuration_types', {})
        configuration_type_key = values.get('configuration_type_key', {})
        configuration_key = values.get('configuration_key', {})

        valid_configuration_types = configuration_types.keys()

        if values[configuration_type_key] not in valid_configuration_types:
            raise ValueError(
                f"Unknown configuration_type: {values[configuration_type_key]}")
        try:
            cfg_object_type = configuration_types.get(
                values[configuration_type_key])
            updated_configuration = [
                cfg_object_type(**c)
                for c in values[configuration_key]
            ]
        except KeyError as wrong_ref:
            raise ValueError(
                f"Cannot load plugin configuration! "
                f"due to error: '{repr(wrong_ref)}'"
            )
        return {**values, configuration_key: updated_configuration}


class ConversionStep(BaseModel):
    """Represents single conversion step entity"""
    step_name: str
    step_instructions: SinglePluginData

# URLs SECTION:


class SingleUrlSetting(BaseModel):
    """Represents single url setting entity"""
    id: str
    url: str


class UrlsConfiguration(BaseModel):
    """Represents total urls configuration"""
    urls: List[SingleUrlSetting]
