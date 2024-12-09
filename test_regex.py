import re
import unittest

from core.regex_service import PATTERN


class TestRegexHyperlinks(unittest.TestCase):
    pattern = re.compile(PATTERN)

    def test_full_match_valid(self):
        valid_cases = [
            "https://example.com",
            "http://example.com",
            "https://sub.domain.example.com/path/to/resource",
            "http://127.0.0.1:8000",
            "https://example.com?query=param&other=value",
        ]
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertIsNotNone(self.pattern.fullmatch(case))

    def test_full_match_invalid(self):
        invalid_cases = [
            "ftp://example.com",         # Протокол не http/https
            "example.com",               # Отсутствует протокол
            "http:/example.com",         # Неполный протокол
            "https://",                  # Протокол без домена
            "https:// example.com",      # Пробел в URL
            "https://example.com/<>",    # Недопустимые символы
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertIsNone(self.pattern.fullmatch(case))

    def test_search_valid(self):
        strings = [
            "Visit https://example.com for details.",
            "Check http://example.org/resource.",
            "Multiple links: https://a.com and http://b.com.",
        ]
        for string in strings:
            with self.subTest(string=string):
                self.assertIsNotNone(self.pattern.search(string))

    def test_search_invalid(self):
        strings = [
            "No links here.",
            "Just some text http:/invalid-link.",
            "https: //example.com is malformed.",
        ]
        for string in strings:
            with self.subTest(string=string):
                self.assertIsNone(self.pattern.search(string))

    def test_findall(self):
        string = "Links: https://example.com , http://example.org , and https://sub.example.net/path ."
        expected_matches = [
            "https://example.com",
            "http://example.org",
            "https://sub.example.net/path",
        ]
        self.assertEqual(self.pattern.findall(string), expected_matches)

    def test_substitution(self):
        string = "Replace https://example.com and http://example.org with placeholders."
        expected_result = "Replace [LINK] and [LINK] with placeholders."
        result = self.pattern.sub("[LINK]", string)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
