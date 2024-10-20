import unittest

from la import Lexer

"""
Тестирование лексического анализатора
"""


class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()

    def test1(self):
        """
        Тест для действительных чисел. Проверка корректных чисел типа float.
        """
        self.assertEqual(
            self.lexer.tokenize("3.1", True),
            [(4, "3.1", "10", "float")],
        )
        self.assertEqual(
            self.lexer.tokenize(".1", True),
            [(4, ".1", "10", "float")],
        )
        self.assertEqual(
            self.lexer.tokenize("3.2E11", True),
            [(4, "3.2E11", "10", "float")],
        )
        self.assertEqual(
            self.lexer.tokenize(".2E+11", True),
            [(4, ".2E+11", "10", "float")],
        )
        self.assertEqual(
            self.lexer.tokenize("3.2E-11", True),
            [(4, "3.2E-11", "10", "float")],
        )
        self.assertEqual(
            self.lexer.tokenize("3.2e11", True),
            [(4, "3.2e11", "10", "float")],
        )
        self.assertEqual(
            self.lexer.tokenize(".2e12", True),
            [(4, ".2e12", "10", "float")],
        )
        self.assertEqual(
            self.lexer.tokenize(".2e+12", True),
            [(4, ".2e+12", "10", "float")],
        )
        self.assertEqual(
            self.lexer.tokenize(".2e-12", True),
            [(4, ".2e-12", "10", "float")],
        )

    def test2(self):
        """
        Тестирование исключений и обработки ошибок для типа float.
        """
        self.assertEqual(
            self.lexer.tokenize("1.", debug=True),
            ["error", "1.", "Действительное число не может заканчиваться точкой."],
        )
        self.assertEqual(
            self.lexer.tokenize("1.2.1", debug=True),
            [
                "error",
                "1.2.1",
                "В действительном числе не может быть более одной точки.",
            ],
        )
        self.assertEqual(
            self.lexer.tokenize("1E.1", debug=True),
            [
                "error",
                "1E.1",
                "В действительном числе точка не может стоять после порядка.",
            ],
        )
        self.assertEqual(
            self.lexer.tokenize("1.E1", debug=True),
            ["error", "1.E1", "Сразу после точки не может идти порядок."],
        )
        self.assertEqual(
            self.lexer.tokenize("1.1E+1+1", debug=True),
            ["error", "1.1E+1+1", "Лишний знак + или - в токене типа float."],
        )
        self.assertEqual(
            self.lexer.tokenize("1E", debug=True),
            ["error", "1E", "Порядок не может находиться в конце числа."],
        )
        self.assertEqual(
            self.lexer.tokenize("1.2Ee23", debug=True),
            [
                "error",
                "1.2Ee23",
                "В действительном числе порядок не может быть указан более одного раза.",
            ],
        )

    def test3(self):
        """
        Тест для целых чисел (int).
        """
        self.assertEqual(
            self.lexer.tokenize("123", debug=True), [(4, "123", "10", "int")]
        )
        self.assertEqual(
            self.lexer.tokenize("10000", debug=True), [(4, "10000", "10", "int")]
        )
        self.assertEqual(
            self.lexer.tokenize("011101b", debug=True), [(4, "011101", "2", "int")]
        )
        self.assertEqual(self.lexer.tokenize("1B", debug=True), [(4, "1", "2", "int")])
        self.assertEqual(
            self.lexer.tokenize("17o", debug=True), [(4, "17", "8", "int")]
        )
        self.assertEqual(
            self.lexer.tokenize("2afh", debug=True), [(4, "2af", "16", "int")]
        )
        self.assertEqual(
            self.lexer.tokenize("10d", debug=True), [(4, "10", "10", "int")]
        )

    def test4(self):
        """
        Тестирование исключений и обработки ошибок для типа int.
        """
        self.assertEqual(
            self.lexer.tokenize("12b", debug=True),
            ["error", "12b", "Недопустимые символы для двоичной системы."],
        )
        self.assertEqual(
            self.lexer.tokenize("18o", debug=True),
            ["error", "18o", "Недопустимые символы для восьмеричной системы."],
        )

    def test5(self):
        """
        Тестирование идентификаторов.
        """
        self.assertEqual(self.lexer.tokenize("abc", debug=True), [(3, 0)])
        self.assertEqual(
            self.lexer.tokenize("abc abc ab c abc a", debug=True),
            [(3, 0), (3, 0), (3, 1), (3, 2), (3, 0), (3, 3)],
        )
        self.assertEqual(self.lexer.tokenize("ABC", debug=True), [(3, 0)])
        self.assertEqual(self.lexer.tokenize("aBC", debug=True), [(3, 0)])
        self.assertEqual(self.lexer.tokenize("hh", debug=True), [(3, 0)])
        self.assertEqual(self.lexer.tokenize("h12b", debug=True), [(3, 0)])
        self.assertEqual(self.lexer.tokenize("a212gfh", debug=True), [(3, 0)])


    def test6(self):
        """
        Тестирование исключений и обработки ошибок для идентификаторов.
        """
        self.assertEqual(
            self.lexer.tokenize("12x", debug=True),
            [
                "error",
                "12x",
                "Идентификатор не может начинаться с числа или разделителя.",
            ],
        )
        self.assertEqual(
            self.lexer.tokenize("hлxxx", debug=True),
            [
                "error",
                "hлxxx",
                "Неизвестные символы в идентификаторе.",
            ],
        )


if __name__ == "__main__":
    unittest.main()
