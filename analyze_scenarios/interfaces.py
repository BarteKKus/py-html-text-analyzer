import abc
from typing import List
from configuration.urls_cfg_json_loader import UrlsConfiguration
from configuration.plugins_cfg_json_loader import ConversionStep


class AnalyzeScenario(metaclass=abc.ABCMeta):
    """Analyze scenario interface"""

    @abc.abstractmethod
    def __init__(
        self,
        urls_cfg: UrlsConfiguration,
        plugins_cfg: List[ConversionStep]
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self) -> bool:
        """Returns True when execution is finished"""
        raise NotImplementedError
