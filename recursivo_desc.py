from Consts import Consts
from Error import Error

""" i é int
 E-> iK
 K -> +iK
 K -> 
"""

''' BoLD
S -> *K
K -> *T
T ->
'''
class RecDescendente:
    def __init__(self, toks):
        self.tokens = toks
        self.id = -1
        self.current = None
        self.txt = '' #log
    
    def start(self):
        self.nextToken()
        a, e = self.E()
        if self.currentTok().type != Consts.EOF:
            return None, (e+":Erro nao $ no final")
        return a, e
    
    def currentTok(self): return self.current

    def nextToken(self):
        self.id += 1
        if self.id<len(self.tokens):
            self.current = self.tokens[self.id]
        return self.current # pode ser que precise
    
    def E(self):
        if self.currentTok().type == Consts.INT:
            self.txt += "i"
            self.nextToken()
            a, e = self.K()
            return a, e
        return None, "Falha E(), precisa iniciar com inteiro"
    
    def K(self):

        print(self.currentTok())
        if self.currentTok().type == Consts.PLUS:
            self.nextToken()
            if self.currentTok().type == Consts.INT:
                self.nextToken()
                self.txt += "+i"
                a, e = self.K()
                return self.txt, e
            else:
                return self.txt, ": nao eh inteiro no final"

        self.txt += "e" #adicionando vazio
        return self.txt, None # quando fica vazio
