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
        ]
        self.numbers = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "0",
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
        if not set(token).intersection(self.vocabilary):
            return False, False

        if not token in identificators:
            identificators.append(token)
        token_id = identificators.index(token)

        return (3, token_id), identificators

    def find_numbers(self, token: str) -> tuple[int, str] | bool:
        """
        Проверка токена на принадлежность к группе чисел (4).
        Определение системы счисления.

        Варианты чисел: двоичное (1), восьмеричное (2), десятеричное (3), шестнадцатиричное (4)
        Действительные числа: <числовая_сторка><порядок> | [<числовая_строка>].<число>[<порядок>]

        """

        """
        Проверка на принадлежность к целым числам (integer).
        Определение системы счисления (ns), типа токена (tt).
        """

        tt = False
        ns = False

        p_count = 0
        e_count = 0
        E_count = 0

        for _ in token:
            if _ == ".":
                if e_count > 0 or E_count > 0:
                    return (4, "err", "err")
                p_count += 1
                if p_count > 1:
                    return False
            elif _ == "e":
                e_count += 1
            elif _ == "E":
                E_count += 1

        # print(p_count, e_count, E_count)

        if e_count + e_count == 1 or p_count == 1:
            tt = "float"
            ns = "10"
            return (4, token, ns, tt)

        # if "." in token or ("e" in token and set(token[:-1]).intersection(self.vocabilary)):
        #     pass

        # print(set(token[:-1]))

        if (token[-1] == "B" or token[-1] == "b") and not set(token[:-1]).intersection(
            self.vocabilary
        ):
            ns = "2"
        elif (token[-1] == "O" or token[-1] == "o") and not set(
            token[:-1]
        ).intersection(self.vocabilary):
            ns = "8"
        elif (token[-1] == "H" or token[-1] == "h") and not set(
            token[:-2]
        ).intersection(self.vocabilary):
            ns = "16"
        elif not set(token[:-1]).intersection(self.vocabilary) and len(token) > 1 or not set(token).intersection(self.vocabilary):
            if token[-1] == "D" or token[-1] == "d":
                token = token[:-1]
            ns = "10"
            tt = "int"
            return (4, token, ns, tt)

        tt = "int"
        token = token[:-1]

        return (4, token, ns, tt)

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

            token = Lexer.find_numbers(self, _)
            # print(_, token)
            if token[2]:
                new_data.append(token)
                continue

            # TODO Сделать проверку на 2, 8, 10 и 16 -ричные системы счисления, разделение на действительные и целые числа

            """
            Проверка на принадлежность токена к группе идентификаторов (3).
            """
            token, new_identificators = Lexer.find_identificators(
                self, _, identificators
            )

            if token:
                # print(3, token)
                new_data.append(token)
                identificators = (
                    new_identificators if new_identificators else identificators
                )
                continue

            new_data.append(("undefined", _))
            
            print(new_data)

        return new_data
