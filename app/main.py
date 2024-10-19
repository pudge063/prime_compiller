import la

path = "examples"

file = "all_errors.psuti"

lexer = la.Lexer()

tokens = lexer.tokenize(path + "/" + file)

print(tokens)
