import time

# Dicionário com a tradução para Código Morse Internacional
MORSE_CODE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    " ": " ",
}


class Interpreter:
    """
    Percorre a AST e executa os comandos MorseScript.
    """

    def __init__(self, ast):
        self.ast = ast
        self.velocidade_wpm = 20

    def _get_duracao_ponto_s(self):
        """Calcula a duração de um ponto em segundos baseado na velocidade (Word Per Minute)."""
        return 1.2 / self.velocidade_wpm

    def visit(self, node):
        """Método genérico que chama o método específico para o tipo de nó."""
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node)

    def no_visit_method(self, node):
        raise Exception(f"Nenhum método visit_{type(node).__name__} encontrado")

    def visit_ProgramaNode(self, node):
        for comando in node.comandos:
            self.visit(comando)

    def visit_VelocidadeNode(self, node):
        self.velocidade_wpm = node.valor
        print(f"[CONFIG: Velocidade ajustada para {self.velocidade_wpm} WPM]\n")

    def visit_PausaNode(self, node):
        duracao_s = node.valor / 1000.0
        print(f"[PAUSA: {duracao_s:.2f} segundos...]\n")
        time.sleep(duracao_s)

    def visit_RepitaNode(self, node):
        for i in range(node.vezes):
            print(f"-- Início da Repetição {i + 1}/{node.vezes} --\n")
            for comando in node.bloco:
                self.visit(comando)
            print(f"-- Fim da Repetição {i + 1}/{node.vezes} --\n")

    def visit_TextoNode(self, node):
        texto = node.valor.upper()
        duracao_ponto = self._get_duracao_ponto_s()

        print(f'Transmitindo: "{node.valor}"')

        for i, char in enumerate(texto):
            if char == " ":
                print("  /  ", end="", flush=True)
                time.sleep(7 * duracao_ponto)
                continue

            codigo_morse = MORSE_CODE_DICT.get(char)
            if not codigo_morse:
                print(
                    f"[ERRO: Caractere '{char}' não pode ser transmitido]",
                    end="",
                    flush=True,
                )
                continue

            print(f"{codigo_morse} ", end="", flush=True)

            time.sleep(len(codigo_morse) * duracao_ponto * 1.5)

            if i < len(texto) - 1 and texto[i + 1] != " ":
                time.sleep(3 * duracao_ponto)

        print("\n[TRANSMISSÃO COMPLETA]\n")
        time.sleep(1)

    def run(self):
        """Inicia a interpretação da AST."""
        self.visit(self.ast)
