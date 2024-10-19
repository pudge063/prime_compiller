import la

path = "examples"

file = "test1.psuti"

lexer = la.Lexer()

tokens = lexer.tokenize(path + "/" + file)

print(tokens)
