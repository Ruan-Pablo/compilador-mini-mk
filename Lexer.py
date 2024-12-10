from Consts import Consts
from Token import Token
from Error import Error

class Lexer:
    def __init__(self, source_code):
        self.code = source_code
        self.current = None
        self.indice = -1
        self.__advance()

    def __advance(self):
        """Avança para o próximo caractere na entrada."""
        self.indice += 1
        self.current = self.code[self.indice] if self.indice < len(self.code) else None

    def __peek(self):
        """Olha o próximo caractere sem avançar."""
        return self.code[self.indice + 1] if self.indice + 1 < len(self.code) else None

    def makeTokens(self):
        """Gera uma lista de tokens a partir do código-fonte."""
        tokens = []
        while self.current is not None:
            if self.current in '\t\n ':
                self.__advance()  # Ignora espaços, tabulações e quebras de linha
            elif self.current == '#' and (self.__peek() == ' ' or self.__peek() == '#'):
                tokens.append(self.__makeHeader())
            elif self.current == '*' and self.__peek() == '*':
                tokens.append(self.__makeBold())
            elif self.current == '_':
                # Verifica se está no início ou se o caractere anterior é um espaço ou quebra de linha
                if self.indice == 0 or self.code[self.indice - 1] in {' ', '\n'}:
                    tokens.append(self.__makeUnder())
                else:
                    tokens.append(self.__makeString())
            elif self.current == '-':
                tokens.append(self.__makeList())
            else:
                tokens.append(self.__makeString())
        tokens.append(Token(Consts.EOF))
        return tokens, None 

    def __makeHeader(self):
        """Reconhece cabeçalhos (ex: # Título, mas não #titulo)."""
        level = 0
        while self.current == '#':
            level += 1
            self.__advance()
        
        # Verifica se há um espaço após os #
        if self.current == ' ':
            self.__advance()  # Consome o espaço
            content = self.__consumeUntilNewline()
            return Token(Consts.HEADER, f"H{level}: {content}")
        else:
            # Se não houver espaço, trata como uma STRING
            return self.__makeString()

    def __makeBold(self):
        """Reconhece texto em negrito delimitado por **, mesmo sem espaços."""
        self.__advance()  # Consome o primeiro '*'
        self.__advance()  # Consome o segundo '*'
        bold_text = ""
        while self.current is not None and not (self.current == '*' and self.__peek() == '*'):
            bold_text += self.current
            self.__advance()
        self.__advance()  # Consome o primeiro '*' de fechamento
        self.__advance()  # Consome o segundo '*' de fechamento
        return Token(Consts.BOLD, bold_text)
    
    def __makeUnder(self):
        """Reconhece texto em itálico delimitado por _, mesmo no início da entrada."""
        self.__advance()  # Consome o '_'
        italic_text = ""
        while self.current is not None and self.current != '_':
            italic_text += self.current
            self.__advance()
        if self.current == '_':  # Confirma o fechamento
            self.__advance()
            return Token(Consts.ITALIC, italic_text)
        # Se não encontrar fechamento, retorna como STRING
        return Token(Consts.STRING, "_" + italic_text)
    
    def __makeList(self):
        """Reconhece listas (ex: - Item)."""
        self.__advance()  # Consome o '-'
        if self.current == ' ':
            self.__advance()
        content = self.__consumeUntilNewline()
        return Token(Consts.LIST, content)

    def __makeString(self):
        """Reconhece qualquer sequência de caracteres não separados por espaço, tabulação ou nova linha como STRING."""
        string_text = ""
        while self.current is not None:
            # Interrompe ao encontrar delimitadores ou espaços
            if self.current in ' \t\n' or \
            (self.current == '*' and self.__peek() == '*') or \
            (self.current == '_' and (self.indice == 0 or self.code[self.indice - 1] in {' ', '\n'})) or \
            self.current == '-':
                break
            string_text += self.current
            self.__advance()
        return Token(Consts.STRING, string_text)

    def __consumeUntil(self, delimiter, stop_on_special=False):
        """Consome caracteres até encontrar o delimitador."""
        result = ""
        while self.current is not None and not self.code[self.indice:].startswith(delimiter):
            if stop_on_special and self.current in ('#', '-', '*'):
                break
            result += self.current
            self.__advance()
        if self.current is not None:
            for _ in delimiter:  # Consome o delimitador
                self.__advance()
        return result

    def __consumeUntilNewline(self):
        """Consome caracteres até encontrar uma nova linha."""
        result = ""
        while self.current is not None and self.current != '\n':
            result += self.current
            self.__advance()
        return result

