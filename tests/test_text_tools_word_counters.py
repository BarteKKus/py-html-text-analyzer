import pytest

from text_postprocessors.text_tools import WordCounters


@pytest.fixture
def counting_words_test_data():
    return [
        {
            'input': ["word_a", "word_b", "word_a", "word_c"],
            'answer': {'word_a': 2, 'word_b': 1, 'word_c': 1}
        },
        {
            'input': ["word_a", "word_a", "word_a"],
            'answer': {'word_a': 3}
        },
        {
            'input': ["a", "b", "a", "b", "b", "b"],
            'answer': {'b': 4, 'a': 2}
        },
        {
            'input': [],
            'answer': {}
        },
    ]


def test_collections_based_words_counter(counting_words_test_data):
    """Words counter from WordCounter works ONLY with list of words"""
    for test_case in counting_words_test_data:
        result = WordCounters.collections_based_words_counter(
            test_case['input'])
        assert result == test_case['answer']


def test_plain_words_counter(counting_words_test_data):
    """Words counter from WordCounter works ONLY with list of words"""
    for test_case in counting_words_test_data:
        result = WordCounters.plain_words_counter(test_case['input'])
        assert result == test_case['answer']
