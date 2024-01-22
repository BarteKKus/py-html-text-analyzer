import pytest

from text_postprocessors.text_tools import WordExtractors


@pytest.fixture
def extracting_words_test_data():
    return [
        {
            'input': "this is a test ",
            'answer': ['this', 'is', 'a', 'test']
        },
        {
            'input': "",
            'answer': []
        }
    ]


def test_regex_words_extractor(extracting_words_test_data):
    """Words extractors from WordExtractors works ONLY with sanitized text
    - only with digits and letters with empty spaces"""
    for test_case in extracting_words_test_data:
        result = WordExtractors.regex_words_extractor(test_case['input'])
        assert result == test_case['answer']


def test_plain_words_extractor(extracting_words_test_data):
    """Words extractors from WordExtractors works ONLY with sanitized text
    - only with digits and letters with empty spaces"""
    for test_case in extracting_words_test_data:
        result = WordExtractors.plain_words_extractor(test_case['input'])
        assert result == test_case['answer']
