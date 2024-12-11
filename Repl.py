from Lexer import Lexer
from cmd import Cmd

class Repl(Cmd):
    prompt = 'UFC> '
    intro = "Bem vindo!\nDigite\n :h para ajuda\n :q para sair\n :s para exemplos de teste\n :r para rodar código predefinido!"

    def do_exit(self, inp):
        return True

    def help_exit(self):
        print('Digite\n :q para sair\n :s para ver exemplos de teste\n :r para rodar código predefinido!')
        return False

    def emptyline(self):  # Desabilita repetição do último comando
        pass

    def _s(self):
        print("Exemplos de teste:")
        print('1. # Título com **negrito** e _itálico_')
        print('2. Texto normal _itálico_ **negrito**')
        print('3. - Lista com _itens em itálico_ e **negrito**')
        print('4. **Sem fechamento')
        return False

    def _r(self):
        predefined_code = """# Título com **negrito** e _itálico_
Texto normal com **negrito** e _itálico_.
- Item 1 com _itálico_
- Item 2 com **negrito**
"""
        print("Executando código predefinido...")
        self.run(predefined_code)
        return False

    def default(self, inp):
        if inp == ':q':
            return self.do_exit(inp)
        elif inp == ':h':
            return self.help_exit()
        elif inp == ':s':
            return self._s()
        elif inp == ':r':
            return self._r()
        self.analisador(inp)
        return False

    do_EOF = do_exit
    help_EOF = help_exit

    def imprimir(self, classe, tokens):
        print(f"{type(classe).__name__}:")
        for i in tokens:
            print(i)

    def run(self, linha):
        lexer = Lexer(linha)
        tokens, error = lexer.makeTokens()
        if error:
            print(f"Erro: {error}")
            return None, error

        self.imprimir(lexer, tokens)
        return tokens, None

    def analisador(self, linha):
        resultado, error = self.run(linha)
        if error:
            print(f"Log de Erro: {error}")
