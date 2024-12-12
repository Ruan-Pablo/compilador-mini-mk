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
        self.indice += 1
        self.current = self.code[self.indice] if self.indice < len(self.code) else None

    def __peek(self):
        return self.code[self.indice + 1] if self.indice + 1 < len(self.code) else None

    def makeTokens(self):
        tokens = []
        while self.current is not None:
            if self.current in '\t\n ':
                self.__advance()  
            elif self.current == '#' and (self.__peek() == ' ' or self.__peek() == '#'): # HEADER
                # Verifica se está no início ou se o caractere anterior é um espaço ou quebra de linha
                if self.indice == 0 or self.code[self.indice - 1] in {'\n'}:
                    tokens.append(self.__makeHeader())
                else:
                    tokens.append(self.__makeString())
            elif self.current == '*' and self.__peek() == '*': # BOLD
                tokens.append(self.__makeBold())
            elif self.current == '_': # ITALIC
                if self.indice == 0 or self.code[self.indice - 1] in {' ', '\n'}:
                    tokens.append(self.__makeUnder())
                else:
                    tokens.append(self.__makeString())
            elif self.current == '-': # LIST
                if self.indice == 0 or self.code[self.indice - 1] in {'\n'}:
                    tokens.append(self.__makeList())
                else:
                    tokens.append(self.__makeString())
            else:
                tokens.append(self.__makeString())
        tokens.append(Token(Consts.EOF))
        return tokens, None


    def __makeHeader(self):
        level = 0
        while self.current == '#':
            level += 1
            self.__advance()
        
        # Verifica e consome o espaço após os #
        if self.current == ' ':
            self.__advance()
            tokens = []
            while self.current is not None and self.current != '\n':
                if self.current == '*' and self.__peek() == '*':
                    tokens.append(self.__makeBold())
                elif self.current == '_' and (self.indice == 0 or self.code[self.indice - 1] in {' ', '\n'}):
                    tokens.append(self.__makeUnder())
                elif self.current not in '\t\n ':
                    tokens.append(self.__makeString())
                else:
                    self.__advance()
            return Token(Consts.HEADER, {"level": level, "content": tokens})
        else:
            # Se não houver espaço, trata como uma STRING
            return self.__makeString()


    
    def __makeList(self):
        self.__advance()  # Consome o '-'
        if self.current == ' ':
            self.__advance() 
            tokens = []
            while self.current is not None and self.current != '\n':
                if self.current == '*' and self.__peek() == '*':
                    tokens.append(self.__makeBold())
                elif self.current == '_' and (self.indice == 0 or self.code[self.indice - 1] in {' ', '\n'}):
                    tokens.append(self.__makeUnder())
                elif self.current not in '\t\n ':
                    tokens.append(self.__makeString())
                else:
                    self.__advance()
            return Token(Consts.LIST, {"content": tokens})
        else:
            # Se não houver espaço, trata como uma STRING
            return self.__makeString()

    def __makeBold(self):
        self.__advance()  # Consome o primeiro '*'
        self.__advance()  # Consome o segundo '*'

        bold_text = ""
        while self.current is not None:
            if self.current == '*' and self.__peek() == '*':
                self.__advance()  # Consome um '*'
                if self.__peek() == '*':  # verifica se o proximo eh * para checar a sequencia de *'s
                    bold_text += "*"  # Caso seja eh parte do texto
                    
                else:
                    self.__advance()
                    return Token(Consts.BOLD, bold_text)
            else:
                bold_text += self.current
                self.__advance()

        # Se não encontrar delimitador de fechamento, trata como STRING
        return Token(Consts.STRING, "**" + bold_text)
    
    def __makeUnder(self):
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

    def __makeString(self):
        string_text = ""
        while self.current is not None:
            # Interrompe ao encontrar delimitadores ou espaços
            if self.current in ' \t\n' or \
            (self.current == '*' and self.__peek() == '*') or \
            (self.current == '_' and (self.indice == 0 or self.code[self.indice - 1] in {' ', '\n'})):
                break
            string_text += self.current
            self.__advance()
        return Token(Consts.STRING, string_text)
