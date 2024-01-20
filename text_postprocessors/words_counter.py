from typing import Callable, List, Dict

from text_postprocessors.text_tools import WordCounters, WordExtractors


def simple_words_counter(
    text: str,
    words_extractor: Callable[[str], List[str]] = (
        WordExtractors.plain_words_extractor
    ),
    words_calculator: Callable[[List[str]], Dict[int, str]] = (
        WordCounters.plain_words_counter
    )
) -> Dict[str, int]:
    """Function counts words in text.

    Returns:
        Dict[str,int]: For example: {'apple':129,'song':875,'table:87'}
    """
    return words_calculator(words_extractor(text))
