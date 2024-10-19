import unittest

from la import Lexer

"""
Тестирование лексического анализатора
"""


class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()

    # def test1(self):
    #     self.assertEqual(
    #         self.lexer.tokenize("examples/test1.psuti"),
    #         [
    #             (1, 1),
    #             (2, 24),
    #             (1, 2),
    #             (1, 4),
    #             ("undefined", "x"),
    #             (2, 23),
    #             ("undefined", "y"),
    #             (1, 5),
    #             (2, 24),
    #             ("undefined", "x"),
    #             (1, 8),
    #             ("undefined", "2"),
    #             (2, 24),
    #             ("undefined", "y"),
    #             (1, 8),
    #             ("undefined", "x"),
    #             ("undefined", ""),
    #             (2, 10),
    #             ("undefined", "2"),
    #             (2, 24),
    #             (1, 18),
    #             ("undefined", "y"),
    #             (2, 24),
    #             (1, 3),
    #         ],
    #     )

    def test2(self):
        self.assertEqual(
            self.lexer.tokenize("x assign 2;", True),
            [(3, 0), (1, 8), ("undefined", "2"), (2, 24)],
        )

    def test3(self):
        self.assertEqual(
            self.lexer.tokenize("x y y x y;", True),
            [(3, 0), (3, 1), (3, 1), (3, 0), (3, 1), (2, 24)],
        )

    def test4(self):
        self.assertEqual(
            self.lexer.tokenize("12 1 3", True),
            [("undefined", "12"), ("undefined", "1"), ("undefined", "3")],
        )


if __name__ == "__main__":
    unittest.main()
