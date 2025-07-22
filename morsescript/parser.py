from .lexer import TipoToken


# --- AST (Abstract Syntax Tree) ---
class ASTNode:
    pass


class ProgramaNode(ASTNode):
    def __init__(self, comandos):
        self.comandos = comandos


class ComandoNode(ASTNode):
    pass


class TextoNode(ComandoNode):
    def __init__(self, valor_string):
        self.valor = valor_string


class VelocidadeNode(ComandoNode):
    def __init__(self, valor_numero):
        self.valor = valor_numero


class PausaNode(ComandoNode):
    def __init__(self, valor_numero):
        self.valor = valor_numero


class RepitaNode(ComandoNode):
    def __init__(self, vezes, bloco_comandos):
        self.vezes = vezes
        self.bloco = bloco_comandos


class Parser:
    """
    Analisador Sintático para MorseScript. Constrói uma AST.
    """

    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.proximo_token()

    def erro(self, tipo_esperado):
        raise SyntaxError(
            f"Erro de sintaxe: esperado {tipo_esperado}, mas encontrado {self.token_atual.tipo}"
        )

    def consumir(self, tipo_token):
        """Consome o token atual se for do tipo esperado, e avança para o próximo."""
        if self.token_atual.tipo == tipo_token:
            self.token_atual = self.lexer.proximo_token()
        else:
            self.erro(tipo_token)

    def parse_comando(self):
        """Analisa um único comando."""
        tipo = self.token_atual.tipo

        if tipo == TipoToken.TEXTO:
            self.consumir(TipoToken.TEXTO)
            valor_string = self.token_atual.valor
            self.consumir(TipoToken.STRING)
            return TextoNode(valor_string)

        if tipo == TipoToken.VELOCIDADE:
            self.consumir(TipoToken.VELOCIDADE)
            valor_numero = self.token_atual.valor
            self.consumir(TipoToken.NUMERO)
            return VelocidadeNode(valor_numero)

        if tipo == TipoToken.PAUSA:
            self.consumir(TipoToken.PAUSA)
            valor_numero = self.token_atual.valor
            self.consumir(TipoToken.NUMERO)
            return PausaNode(valor_numero)

        if tipo == TipoToken.REPITA:
            self.consumir(TipoToken.REPITA)
            vezes = self.token_atual.valor
            self.consumir(TipoToken.NUMERO)
            self.consumir(TipoToken.ABRE_COLCHETE)

            bloco_comandos = []
            while self.token_atual.tipo != TipoToken.FECHA_COLCHETE:
                bloco_comandos.append(self.parse_comando())

            self.consumir(TipoToken.FECHA_COLCHETE)
            return RepitaNode(vezes, bloco_comandos)

        return None

    def parse(self):
        """Analisa o programa inteiro e retorna a raiz da AST."""
        comandos = []
        while self.token_atual.tipo != TipoToken.FIM_DE_ARQUIVO:
            comando = self.parse_comando()
            if comando:
                comandos.append(comando)
            else:
                break

        return ProgramaNode(comandos)
