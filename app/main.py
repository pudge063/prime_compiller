import la

path = "tests"

file = "identificators.psuti"

lexer = la.Lexer()

tokens = lexer.tokenize(path + "/" + file)

print(tokens)
