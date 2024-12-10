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
        """Reconhece cabeçalhos e processa conteúdo interno para negrito e itálico."""
        level = 0
        while self.current == '#':
            level += 1
            self.__advance()
        
        # Verifica e consome o espaço após os #
        if self.current == ' ':
            self.__advance()  # Avança para o conteúdo do título
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
            # Retorna o título como um conjunto de tokens
            return Token(Consts.HEADER, {"level": level, "content": tokens})
        else:
            # Se não houver espaço, trata como uma STRING
            return self.__makeString()

    def __makeBold(self):
        """Reconhece texto em negrito delimitado por ** no início e ** no final."""
        self.__advance()  # Consome o primeiro '*'
        self.__advance()  # Consome o segundo '*'

        bold_text = ""
        while self.current is not None:
            # Verifica se encontrou exatamente dois asteriscos no fechamento
            if self.current == '*' and self.__peek() == '*':
                # Verifica se após os dois asteriscos não há outro '*'
                self.__advance()  # Consome o primeiro '*' do fechamento

                if self.__peek() == '*':  # verifica se o proximo eh * para checar a sequencia de *'s
                    bold_text += "*"  # Caso seja parte do texto
                    
                else:
                    self.__advance()
                    return Token(Consts.BOLD, bold_text)

                    # bold_text += "**"  # Caso seja parte do texto
            else:
                # Adiciona caracteres ao texto
                bold_text += self.current
                self.__advance()

        # Se não encontrar delimitador de fechamento, trata como STRING
        return Token(Consts.STRING, "**" + bold_text)
    
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
            self.__advance()  # Avança para o conteúdo do título
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
            # Retorna o título como um conjunto de tokens
            return Token(Consts.LIST, {"content": tokens})
            # return Token(Consts.HEADER, {"level": level, "content": tokens})
        else:
            # Se não houver espaço, trata como uma STRING
            return self.__makeString()

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


    def __consumeUntilNewline(self):
        """Consome caracteres até encontrar uma nova linha."""
        result = ""
        while self.current is not None and self.current != '\n':
            result += self.current
            self.__advance()
        return result

