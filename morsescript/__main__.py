import sys
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


def main():
    if len(sys.argv) != 2:
        print("Uso: python -m morsescript <caminho_para_o_arquivo.morse>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            codigo_fonte = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{caminho_arquivo}'")
        sys.exit(1)

    try:
        lexer = Lexer(codigo_fonte)
        parser = Parser(lexer)
        arvore_ast = parser.parse()
        interpreter = Interpreter(arvore_ast)
        interpreter.run()

    except (ValueError, SyntaxError) as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
