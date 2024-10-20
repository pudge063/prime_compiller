class Lexer:
    """
    Класс лексического анализатора грамматики для разделения полученного кода на токены

    Вход - программа на языке заданной грамматики:

    begin
        (*
         пример комментария
        *)
        var dim x, y #;
        x assign 2;
        y assign x * 2;

        (* вывод результата *)
        displ y;
    end

    Вывод - ожидаемый набор токенов (лексем) грамматики:

    (1, 1), (1, 2), (1, 3), (2, 1), (3, 1), (2, 1), (3, 2), (2, 2), (2, 1), (1, 4), (4, 1), (2, 2) ...

    """

    def __init__(self):
        """
        Инициализация лексического анализатора.
        Инициализация набора токенов ключевых слов, разделителей и логических констант.
        Перевод из json формата в dict ключевых слов, разделителей, логических констант.
        """
        import json

        tokens_path = "app/tokens.json"
        tokens_data = Lexer.open_file(self, tokens_path)
        tokens = json.loads(tokens_data)

        self.keywords = tokens["keywords"]
        self.separators = tokens["separators"]
        self.logical_constants = tokens["logical_constants"]
        self.vocabilary = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "r",
            "s",
            "t",
            "u",
            "w",
            "x",
            "y",
            "z",
            "_",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "G",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "R",
            "S",
            "T",
            "U",
            "W",
            "X",
            "Y",
            "Z",
        ]
        self.numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.float = ["e", "E", "+", "-", "."]
        self.int = [
            "h",
            "H",
            "d",
            "D",
            "b",
            "B",
            "o",
            "O",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
        ]

    def open_file(self, file: str) -> str:
        """
        Фукнция получения кода из файла, в параметрах передаётся $path + $filename типа string (examples/test1.psuti)).
        Возвращает содержимое файла в переменной $data тип string.
        """
        with open(file, "r") as code:
            data = code.read()
        return data

    def split_tokens(data: str) -> list[str]:
        """
        Функция принимает в параметр data типа string набор код программы.
        Возвращает массив без лишних элементов (пробелов, комментариев, переносов).

        Пример:
        Вход: "begin (* пример комментария *) var dim x #; x assert 2; displ x; end"
        Выход:["begin", "(*", "пример", "комментария", "*)", "var", "dim", "x", "#;", "x", "assert", "2;", "displ", "x;", "end"]
        """
        return data.split()

    def remove_comments(data: list[str]) -> list[str]:
        """
        Функция удаляет все комментарии в программе, заключенные в "(* *)".
        Принимает параметр data типа list из строк, возвращает тип list из строк.

        Пример:
        Вход: ["begin", "(*", "пример", "комментария", "*)", "var", "dim", "x", "#;", "x", "assert", "2;", "displ", "x;", "end"]
        Выход: ["begin", "var", "dim", "x", "#;", "x", "assert", "2;", "displ", "x;", "end"]
        """
        oc = False
        new_data = []
        for _ in data:
            if oc and _ == "*)":
                oc = False
            elif oc:
                continue
            elif _ == "(*":
                oc = True
            else:
                new_data.append(_)
        return new_data

    def split_separators(self, data: list[str]):
        """
        Функция для отделения разделителей от ключевых слов, переменных, чисел и идентификаторов.
        Принимает параметр data типа list[str], возвращает list[str].

        Пример:
        Вход: ["begin", "var", "dim", "x", "#;", "x", "assert", "2;", "displ", "x;", "end"]
        Выход:  ["begin", "var", "dim", "x", "#", ";", "x", "assert", "2", ";", "displ", "x", ";", "end"]
        """
        new_data = []

        for _ in data:
            if len(_) > 1 and _[-1] in self.separators:
                new_data.append(_[:-1])
                new_data.append(_[-1])
            else:
                new_data.append(_)

        return new_data

    """
    Поиск по таблицам токенов (лексем) и возврат кортежей вида (token_group, token_id)
    """

    def find_keywords(self, token: str) -> tuple[int, str] | bool:
        """
        Проверка переданного токена на принадлежность к группе keywords (1).
        Функция получает token в параметр token типа string,
        возвращает token_group_id = 1, token_id текущего токена.
        """
        tokens: dict = self.keywords
        if token in tokens:
            return (1, tokens[token])
        else:
            return False

    def find_separators(self, token: str) -> tuple[int, str] | bool:
        """
        Проверка переданного токена на принадлежность к группе separators (2).
        Функция получает token в параметр token типа string,
        возвращает token_group_id = 2, token_id текущего токена.

        Пример:
        Вход: ;
        Выход: (2, 24)

        Вход: x
        Выход: False
        """
        tokens: dict = self.separators
        if token in tokens:
            return (2, tokens[token])
        else:
            return False

    def find_numbers(self, token: str):
        """
        Проверка токена на принадлежность к группе чисел (4).
        Определение системы счисления.

        Варианты чисел: двоичное (1), восьмеричное (2), десятеричное (3), шестнадцатиричное (4)
        Действительные числа: <числовая_сторка><порядок> | [<числовая_строка>].<число>[<порядок>]

        Определение системы счисления (ns), типа токена (tt).
        """

        """
        Список того, что не может быть в числах: set(элементы чисел) - set(алфавит и прочие символы)
        В float числах могут быть 0|1|2|3|4|5|6|7|8|9|0|e|E|.
        В int числах могут быть 0|1|2|3|4|5|6|7|8|9|0|d|D|b|B|h|H
        
        f_exceptions - исключения для float чисел (набор символов, которые не могут быть в действительном числе)
        i_exceptions - исключения для int чисел (набор символов, которые не могут быть в действительном числе)
        """

        def is_sublist(main: list | dict | set, sub: list | dict | set):
            """
            Функция для проверки вхождения одного набора данных в другой.
            Пример:
            Вход: main = [1, 2, 3], sub = [1, 2]
            Вывод: True
            """
            for _ in sub:
                if not _ in main:
                    return False
            return True

        f_exceptions = set(self.vocabilary + [","]) - (set(self.numbers + self.float))
        i_exceptions = set(self.vocabilary + list(self.separators)) - (
            set(self.numbers + self.int)
        )

        """
        Пропуск случаев, когда в токене есть символы, которые не могут быть в числах
        """
        if set(token).intersection(f_exceptions.intersection(i_exceptions)):
            return token, "Skip"

        tt = None  # тип токена
        ns = None  # система счисления

        """
        Разделение на int и float
        
        Правила для float:
        Токен принадлежит к действительным числам, если его символы входят в числа и спецсимволы float (+, -, e, E, .),
        при этом обязательно должна быть либо точка, либо e | E (в единственном экземпляре).
        
        Плюс и минус - знак порядка, может либо отсутствовать, либо присутствовать. Знак может быть только после E | eps.
        
        Точка может быть в начале числа, тогда подразумевается, что целая часть равна 0, после точки обязательно должна быть
        числовая строка. Указание порядка не обязательно, если есть точка.
        
        
        Правила для int:
        Токен принадлежит к целым числам, если его символы входят в числа и в числа и спецсимволы int:
        b|B - двоичная, o|O - восьмеричная, h|H - шестнадцатеричная, d|D|eps - десячичная система
        
        В двоичной системе могут быть только числа 0|1
        В восьмеричной могут быть числа 0|1|2|3|4|5|6|7
        В шестнадцатеричной могут быть числа 0|1|2|3|4|5|6|7|8|9|0 и символы A|B|C|D|E|F|a|b|c|d|e|f
        """

        if (
            is_sublist(self.float + self.numbers, set(token))
            and not set(token).intersection(f_exceptions)
            and set(token).intersection(["e", "E", "."])
        ):
            tt = "float"
        elif set(token).intersection(self.int + self.numbers) and not set(
            token
        ).intersection(i_exceptions):
            tt = "int"
        else:
            return token, "Skip"
        # print(token, tt)

        """
        Проверка на принадлежность к float числам. Нужно проверить, чтобы число подходило под правила:
        <действительное>::=<числовая_строка><порядок>|[<числовая_строка>].<числовая_строка>[<порядок>]
        <числовая_строка>::= {/ <цифра> /}
        <порядок>::= (E|e)[+|-] <числовая_строка>
        
        Проверка, чтобы было не больше 1й точки в числе, чтобы не было букв в первой части,
        чтобы не было больше 1й буквы e|E, вывод ошибки при наличии двух точек или если E стоит до точки.
        """
        if tt == "float":
            # print(token, tt)
            p_count = 0
            e_count = 0
            E_count = 0
            plus_count = 0
            minus_count = 0
            num_after_point = False

            # print(f_exceptions)
            # print(i_exceptions)

            """
            Поиск всех возможных ошибок в действительном числе.
            1. Точка не может стоять в конце числа float, после точки обязательно должна быть числовая строка.
            2. Порядок обя
            """

            if "." == token[-1]:
                return (
                    token,
                    "Действительное число не может заканчиваться точкой.",
                ), "Error"

            if "." in token and (
                ("e" in token)
                and list(token).index("e") < list(token).index(".")
                or ("E" in token)
                and list(token).index("E") < list(token).index(".")
            ):
                return (
                    token,
                    "В действительном числе точка не может стоять после порядка.",
                ), "Error"

            for _ in token:
                if _ == ".":
                    if p_count == 1:
                        return (
                            token,
                            "В действительном числе не может быть более одной точки.",
                        ), "Error"
                    p_count += 1
                elif p_count == 1 and _ in self.numbers:
                    num_after_point = True
                if _ in ["e", "E"]:
                    if num_after_point == False and "." in token:
                        return (
                            token,
                            "Сразу после точки не может идти порядок.",
                        ), "Error"
                    elif _ == "e":
                        e_count += 1
                    elif _ == "E":
                        E_count += 1
                elif _ == "+":
                    plus_count += 1
                    if plus_count > 1:
                        return (
                            token,
                            "Лишний знак + или - в токене типа float.",
                        ), "Error"
                elif _ == "-":
                    minus_count += 1
                    if minus_count > 1:
                        return (
                            token,
                            "Лишний знак + или - в токене типа float.",
                        ), "Error"
                elif (_ == "+" or _ == "-") and (e_count == 0 and E_count == 0):
                    return (
                        token,
                        "Знак + или - не может стоять до идентификатора порядка E или e.",
                    ), "Error"
                elif _ in f_exceptions:
                    return token, "Skip"

            # print(p_count, e_count, E_count, plus_count, minus_count)

            if p_count == 0 and e_count + E_count > 1:
                return token, "Skip"

            if (
                "e" in token
                and (token.index("e") == 0 or token.index("e") == len(token) - 1)
                or "E" in token
                and (token.index("E") == 0 or token.index("E") == len(token) - 1)
            ):
                return (
                    token,
                    "Порядок не может находиться в конце или в начале числа.",
                ), "Error"

            if (
                e_count + E_count == 1
                or p_count == 1
                and e_count + E_count < 2
                and token[-1] != "."
                and token[-1] != "E"
                and token[-1] != "e"
            ):
                tt = "float"
                ns = "10"
                return (4, token, ns, tt), "Pass"
            elif e_count + E_count > 1 and p_count == 1:
                return (
                    token,
                    "В действительном числе порядок не может быть указан более одного раза.",
                ), "Error"

            # if "." in token or ("e" in token and set(token[:-1]).intersection(self.vocabilary)):
            #     pass

            # print(set(token[:-1]))

        """
        Работа с целыми числами (int). Выделение последнего символа токена, проверка на
        принаждежность к двоичному, восьмеричному или шеснадцатеричному числу.
        
        Случаи 2, 8, 16 системы – конец токена равен B|b => 2, O|o => 8, H|h => 16.
        Десятичное число, если в токене нет символов алфавита нетерминалов, последний символ может быть D|d|eps.
        """

        if tt == "int":
            if set(token).intersection(i_exceptions):
                return (4, False, False), "Skip"
            if token[-1] == "B" or token[-1] == "b":
                if is_sublist(self.numbers[:2], token[:-1]):
                    ns = "2"
                    token = token[:-1]
                    return (4, token, ns, tt), "Pass"
                elif set(token[:-1]).intersection(self.vocabilary):
                    return (token), "Skip"
                else:
                    return (
                        token,
                        "Недопустимые символы для двоичной системы.",
                    ), "Error"
            elif token[-1] == "O" or token[-1] == "o":
                if is_sublist((self.numbers[:8]), set(token[:-1])):
                    ns = "8"
                    token = token[:-1]
                    return (4, token, ns, tt), "Pass"
                elif is_sublist((self.numbers[:]), set(token[:-1])):
                    return (
                        token,
                        "Недопустимые символы для восьмеричной системы.",
                    ), "Error"
                else:
                    return token, "Skip"
            elif token[-1] == "H" or token[-1] == "h":
                if is_sublist(self.numbers + self.int[8:], set(token[:-1])):
                    if not token[0] in self.numbers:
                        return (token), "Skip"
                    ns = "16"
                    token = token[:-1]
                    return (4, token, ns, tt), "Pass"
            elif (
                (
                    not set(token[:-1]).intersection(self.vocabilary)
                    and len(token) > 1
                    or not set(token).intersection(self.vocabilary)
                )
                and not set(token).intersection(["."])
                and not (token[-1] == "E" or token[-1] == "e")
            ):
                if token[-1] == "D" or token[-1] == "d":
                    token = token[:-1]
                    ns = "10"
                    return (4, token, ns, tt), "Pass"
                elif str(token[-1]) in self.numbers:
                    ns = "10"
                    return (4, token, ns, tt), "Pass"
                else:
                    return token, "Skip"
            else:
                return token, "Skip"

            # tt = "int"
            # token = token[:-1]

            # return (4, token, ns, tt), "Pass"

    def find_identificators(self, token: str, identificators: list):
        """
        Проверка токена на принадлежность группе идентификаторов (3).

        Фукнция получает token в параметр token типа string,
        и массив существующих идентификаторов типа dict,
        возвращает token_group_id = 3, token_id текущего токена.

        Если идентификатор уже встречался, надо поднять номер этого идентификатора из массива, если он существует.


        Кейсы идентификатора:
        1. abc a b x xy
        2. y1 a22 z222
        3. 2a 33bba
        4. 2a2 4fsd434asfa3 234asd
        5. asf_asf 1_asf 2_asds

        Пример:
        Вход: x
        Выход: (3, 1)

        Вход: a1
        Выход: (3, 1)

        Вход: 12
        Выход: False

        Пример для переиспользования идентификаторов:
        Входная строка для tokenize: ["begin", "var", "dim", "x", "," "y", "#", ";", "x", "isset", "2", ";", ...]
        Шаг с токеном x на позиции 3: token = 'x', identificators = {}, возврат (3, 1)
        Шаг с токеном y на позиции 5: token = 'y', identificators = {'x': '1'}, возврат (3, 2)
        Шаг с токеном x на позиции 8: token = 'x', identificators = {'x': 1, 'y': 2}, возврат: (3, 1)
        """

        def is_sublist(main: list | dict | set, sub: list | dict | set):
            """
            Функция для проверки вхождения одного набора данных в другой.
            Пример:
            Вход: main = [1, 2, 3], sub = [1, 2]
            Вывод: True
            """
            for _ in sub:
                if not _ in main:
                    return False
            return True

        if token[0] in (set(self.numbers + list(self.separators))):
            return (
                (token, "Идентификатор не может начинаться с числа или разделителя."),
                False,
                "Error",
            )

        if not is_sublist(self.vocabilary, set(token)):
            return (token, "Неизвестные символы в идентификаторе."), False, "Error"

        if not token in identificators:
            identificators.append(token)
        token_id = identificators.index(token)

        return (3, token_id), identificators, "Pass"

    def tokenize(self, file: str, debug: str = False) -> list[tuple]:
        """
        Основная функция лексического анализатора.
        Принимает параметр file типа string ($path + "/" + $file).
        Возвращает list кортежей вида (group_id, token_id).

        Параметр debug по умолчанию False, при значении True программа берёт код не из файла,
        а напрямую из переменной file в виде строки. Используется для отладки и unittest.

        Этапы анализа:
        1. Получение кода из файла.
        2. Разделение токенов по пробелам.
        3. Удаление комментариев.
        4. Отделение разделителей от других токенов.
        5. Итерация по массиву токенов и сопоставление токена с группами.
            5.1 Поиск токена в группе ключевых слов (1).
            5.2 Поиск токена в группе разделителей (2).
            5.3 Проверка токена на принадлежность к группе идентификаторов (3).
            5.4 Проверка на принадлежность к группе чисел.
        6. Возврат массива с кортежами вида (group_id, token_id).
        """

        if not debug:
            data = Lexer.open_file(self, file)
        else:
            data = file

        data = Lexer.split_tokens(data)

        data = Lexer.remove_comments(data)

        data = Lexer.split_separators(self, data)

        new_data = []

        identificators = list()

        for _ in data:
            # print(_)
            """
            Проверка на принадлежность токена к группе ключевых слов (1).
            """
            token = Lexer.find_keywords(self, _)
            if token:
                # print(1, token)
                new_data.append(token)
                continue

            """
            Проверка на принадлежность токена к группе разделителей (2).
            """
            token = Lexer.find_separators(self, _)
            if token:
                # print(2, token)
                new_data.append(token)
                continue

            """
            Проверка на принадлежность к группе чисел (4). Определение системы счисления.
            """

            token, status = Lexer.find_numbers(self, _)
            # print(_, token)
            if status == "Pass" and token:
                new_data.append(token)
                continue
            elif status == "Skip":
                """
                Токен не является числом.
                """
                pass
            elif status == "Error":
                """
                Токен распознан как число, но содержит ошибку. Вывод ошибки.
                """
                print(f"Ошибка в токене {token[0]}, описание ошибки: {token[1]}")
                return ["error", token[0], token[1]]
                continue
                # return 0

            # TODO Сделать проверку на 2, 8, 10 и 16 -ричные системы счисления, разделение на действительные и целые числа

            """
            Проверка на принадлежность токена к группе идентификаторов (3).
            """
            token, new_identificators, status = Lexer.find_identificators(
                self, _, identificators
            )

            if token and status == "Pass":
                # print(_)
                # print(3, token)
                new_data.append(token)
                identificators = (
                    new_identificators if new_identificators else identificators
                )
                continue
            elif status == "Error":
                print(f"Ошибка в токене {token[0]}, описание ошибки: {token[1]}.")
                return ["error", token[0], token[1]]
                continue

            # new_data.append(("undefined", _))

            # print(new_data)

        return new_data
