import la

path = "examples"

file = "example1.psuti"

lexer = la.Lexer()

tokens = lexer.tokenize(path + "/" + file)

print(tokens)
