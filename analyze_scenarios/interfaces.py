import abc
from typing import List
from configuration.urls_cfg_json_loader import UrlConfiguration
from configuration.plugins_cfg_json_loader import PluginConfiguration


class AnalyzeScenario(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(
            self,
            urls_cfg: List[UrlConfiguration],
            plugins_cfg: List[PluginConfiguration]
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def execute():
        raise NotImplementedError
