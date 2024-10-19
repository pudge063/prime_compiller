import unittest

from la import Lexer

"""
Тестирование лексического анализатора
"""


class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()

    def test2(self):
        self.assertEqual(
            self.lexer.tokenize("x assign 2;", True),
            [(3, 0), (1, 8), (4, "2", "10", "int"), (2, 24)],
        )

    def test3(self):
        self.assertEqual(
            self.lexer.tokenize("x y y x y;", True),
            [(3, 0), (3, 1), (3, 1), (3, 0), (3, 1), (2, 24)],
        )

    def test4(self):
        self.assertEqual(
            self.lexer.tokenize("12 1 3", True),
            [(4, "12", "10", "int"), (4, "1", "10", "int"), (4, "3", "10", "int")],
        )

    def test5(self):
        self.assertEqual(
            self.lexer.tokenize(
                """
                begin 
                var dim x, y #;
                x assign 2;
                y assign .E+2;
                dim z;
                z assign x + y;
                displ z;
                end
                """,
                True,
            ),
            [
                (1, 1),
                (1, 2),
                (1, 4),
                (3, 0),
                (2, 23),
                (3, 1),
                (1, 5),
                (2, 24),
                (3, 0),
                (1, 8),
                (4, "2", "10", "int"),
                (2, 24),
                (3, 1),
                (1, 8),
                (4, ".E+2", "10", "float"),
                (2, 24),
                (1, 4),
                (3, 2),
                (2, 24),
                (3, 2),
                (1, 8),
                (3, 0),
                (2, 7),
                (3, 1),
                (2, 24),
                (1, 18),
                (3, 2),
                (2, 24),
                (1, 3),
            ],
        )
        
    def test6(self):
        self.assertEqual(
            self.lexer.tokenize("3E.12 3..12d 4.55,12", True),
            [(5, "err", "err"), (5, "err", "err"), ('undefined', '4.55,12')],
        )


if __name__ == "__main__":
    unittest.main()
