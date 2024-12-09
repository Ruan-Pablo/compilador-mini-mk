from Consts import Consts
from Error import Error

'''
E->
Ki
'''

class RecDescendente:
    def __init__(self, toks):
        self.tokens = toks
        self.id = -1
        self.current = None
        self.txt = ''
    def start(self):
        self.nextToken()
        a, e = self.E()
        if self.currentTok().type != Consts.EOF:
            return None, (e+":Erro nao $ no final")
        return a, e