import enum
from collections import namedtuple


class TipoToken(enum.Enum):
    TEXTO = "TEXTO"
    VELOCIDADE = "VELOCIDADE"
    PAUSA = "PAUSA"
    REPITA = "REPITA"

    NUMERO = "NUMERO"
    STRING = "STRING"
    IDENTIFICADOR = "IDENTIFICADOR"

    ABRE_COLCHETE = "["
    FECHA_COLCHETE = "]"

    FIM_DE_ARQUIVO = "FIM_DE_ARQUIVO"


Token = namedtuple("Token", ["tipo", "valor"])


class Lexer:
    """
    Analisadror Léxico para a linguagem MorseScript.
    """

    def __init__(self, codigo_fonte):
        self.codigo = codigo_fonte
        self.posicao = 0
        self.char_atual = (
            self.codigo[self.posicao] if self.posicao < len(self.codigo) else None
        )

        self.PALAVRAS_CHAVE = {
            "TEXTO": Token(TipoToken.TEXTO, "TEXTO"),
            "VELOCIDADE": Token(TipoToken.VELOCIDADE, "VELOCIDADE"),
            "PAUSA": Token(TipoToken.PAUSA, "PAUSA"),
            "REPITA": Token(TipoToken.REPITA, "REPITA"),
        }

    def avancar(self):
        """Avança o ponteiro no código fonte."""
        self.posicao += 1
        if self.posicao < len(self.codigo):
            self.char_atual = self.codigo[self.posicao]
        else:
            self.char_atual = None

    def pular_espacos_e_comentarios(self):
        """Pula espaços em branco,quebras de linha e comentários."""
        while self.char_atual is not None:
            if self.char_atual.isspace():
                self.avancar()
            elif (
                self.posicao + 1 < len(self.codigo)
                and self.char_atual == "/"
                and self.codigo[self.posicao + 1] == "/"
            ):
                while self.char_atual is not None and self.char_atual != "\n":
                    self.avancar()
            else:
                break

    def get_numero(self):
        """Extrai um número inteiro do código."""
        resultado = ""
        while self.char_atual is not None and self.char_atual.isdigit():
            resultado += self.char_atual
            self.avancar()
        return int(resultado)

    def get_string(self):
        """Extrai uma string que tiver entre aspas."""
        self.avancar()
        resultado = ""
        while self.char_atual is not None and self.char_atual != '"':
            resultado += self.char_atual
            self.avancar()
        self.avancar()
        return resultado

    def get_identificador(self):
        """Extrai o identificador ou palavra-chave."""
        resultado = ""
        while self.char_atual is not None and self.char_atual.isalpha():
            resultado += self.char_atual
            self.avancar()
        return self.PALAVRAS_CHAVE.get(
            resultado.upper(), Token(TipoToken.IDENTIFICADOR, resultado)
        )

    def proximo_token(self):
        """Obtém o próximo token do código fonte."""
        while self.char_atual is not None:
            self.pular_espacos_e_comentarios()

            if self.char_atual is None:
                continue

            if self.char_atual.isalpha():
                return self.get_identificador()

            if self.char_atual.isdigit():
                return Token(TipoToken.NUMERO, self.get_numero())

            if self.char_atual == '"':
                return Token(TipoToken.STRING, self.get_string())

            if self.char_atual == "[":
                self.avancar()
                return Token(TipoToken.ABRE_COLCHETE, "[")

            if self.char_atual == "]":
                self.avancar()
                return Token(TipoToken.FECHA_COLCHETE, "]")

            raise ValueError(f"Caractere não reconhecido: {self.char_atual}")

        return Token(TipoToken.FIM_DE_ARQUIVO, None)
