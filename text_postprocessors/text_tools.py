import re
from collections import Counter, defaultdict
from typing import List, Dict, Optional


class WordExtractors:
    """
    Aggregate methods that handle words extraction
    from given string 
    (assuming that string is already sanitized).

    Each method should take text as input and return 
    List of extracted words.
    """

    @staticmethod
    def regex_words_extractor(text: str) -> List[str]:
        return re.findall(
            pattern=r'\b\w+\b',
            string=text
        )

    @staticmethod
    def plain_words_extractor(text: str) -> List[str]:
        words = filter(lambda word: word.isalnum(), text.split())
        return list(words)


class WordCounters:
    """
    Aggregate methods that handle words counting.

    Each method should take list of words as input and return 
    dict that stores counted words like {'word_a':10, 'word_b':2}.
    """
    @staticmethod
    def collections_based_words_counter(
            data_to_count: List[str]) -> Dict[int, str]:
        return dict(Counter(data_to_count))

    @staticmethod
    def plain_words_counter(data_to_count: str) -> Dict[int, str]:
        word_counts = defaultdict(int)
        for word in data_to_count:
            word_counts[word] += 1

        return word_counts


class WordInterpreters:
    """
    Aggregate methods that handle words interpreting like
    presentation,printing,saving to the file etc.

    Each method may expect different input and 
    produce different results if any.
    """
    @staticmethod
    def select_specific_words(
        word_occurrences: Dict[int, str],
        count: Optional[int] = None,
        descending_order: Optional[bool] = False
    ) -> Dict[int, str]:
        """Function selects specified by 'count' parameter number of words
        and sorts them in descending or ascending order by occurence number.

        Args:
            word_occurrences (Dict[int, str]): container with counted 
                words and words strings.
            count (Optional[int], optional): Number of words to include.
                Defaults to None.
            descending_order (Optional[bool], optional): If set to False
                returned order will be ascending. Defaults to False.

        Returns:
            Dict[int, str]: Sorted words regarding occurence number limited to
                count parameter.
        """
        sorted_words = sorted(
            word_occurrences.items(),
            key=lambda item: item[1],
            reverse=descending_order
        )
        return dict(sorted_words[:count])

    @staticmethod
    def print_word_occurences(
        words: Dict[int, str],
        prefix_info: str = "",
        start_numeration_from: int = 1
    ) -> None:
        """Print to the console words occurence in text.

        Args:
            words (Dict[int, str]): container with counted words and words strings
            prefix_info (str, optional): This will be first row in every 
                print line. Defaults to "".
            start_numeration_from (int, optional): Start number for printing
                current number. Defaults to 1.
        Example:
            [   1] ...'https://some_page.com/' | Word:  the  | occurrences: 19
            [   2] ...'https://some_page.com/' | Word:  you  | occurrences: 14
            [   3] ...'https://some_page.com/' | Word:  and  | occurrences: 12
            [   4] ...'https://some_page.com/' | Word:  to   | occurrences: 11
            [   5] ...'https://some_page.com/' | Word:  it   | occurrences: 8
            [   6] ...'https://some_page.com/' | Word:  ONCE | occurrences: 6
        """

        row_idx = start_numeration_from
        longest_word = max(words.keys(), key=lambda word: len(word))
        print("\n")
        for word, occurences in words.items():
            print(
                f"[{row_idx: =4}] {prefix_info:<{len(prefix_info)+1}}| "
                f"Word:  {word:<{len(longest_word)+2}}| "
                f"occurrences:  {occurences}")
            row_idx += 1

    @staticmethod
    def save_word_occurrences_to_txt_file(
        words: Dict[int, str],
        filename: str,
        prefix_info: Optional[str] = None,
    ) -> None:
        """Saves words occurence in text to txt file.

        Args:
            words (Dict[int, str]): container with counted words and words strings,
            filename (str): filename to save results,
            prefix_info (str, optional): This will be first row in txt file. 
                Defaults to "".

        Example:
            Top 10 words from URL 'https://some_page.com/'

            Word:    | Occurrences:
            -------------------------
            the      | 19
            you      | 14
            and      | 12
            to       | 11
            it       | 8
            ONCE     | 6
        """
        longest_word = max(words.keys(), key=lambda word: len(word))
        header = f"Word: {'':<{len(longest_word)-6}} | Occurrences: \n"

        header_to_data_separator = f"{'-' * (len(header)-2)}\n"
        with open(filename, 'w') as file:
            if prefix_info:
                file.write(prefix_info+"\n\n")
            file.write(header)
            file.write(header_to_data_separator)
            for word, occurrences in words.items():
                file.write(
                    f"{word:<{len(longest_word)}} | "
                    f"{occurrences}\n"
                )
        print(f"Saved results for '{prefix_info}' to '{filename}' file.")
