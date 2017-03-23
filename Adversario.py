__author__ = 'Felipe'
from dbmongo import Database
from Utils import Utils

class Adversario:
    def __init__(self):
        self.ident = 0
        self.nome = ""
        self.jogos = 0
        self.vitorias = 0
        self.empates = 0
        self.derrotas = 0
        self.golsFeitos = 0
        self.golsSofridos = 0

    def cadastraAdversarios(self, jogo):
        ret = Adversario().adversarioExiste(jogo)
        Adversario().atualizaEstatisticas(jogo,ret)

    def atualizaEstatisticas(self, jogo, adversario):
        adversario["jogos"] = adversario["jogos"] + 1
        adversario["golsFeitos"] = adversario["golsFeitos"] + int(jogo.placarCruzeiro)
        adversario["golsSofridos"] = adversario["golsSofridos"] + int(jogo.placarAdv)

        if jogo.placarCruzeiro > jogo.placarAdv:
            adversario["vitorias"] = adversario["vitorias"] + 1
        elif jogo.placarCruzeiro == jogo.placarAdv:
            adversario["empates"]  = adversario["empates"]  + 1
        else:
            adversario["derrotas"] = adversario["derrotas"] + 1
        Database().updatedata({"ident":adversario["ident"]}, adversario, "Adversarios")

    def adversarioExiste(self, jogo):
        jsonQuery = {'nome':jogo.adversario}
        cursor = Database().getdata(jsonQuery,0,"Adversarios")
        if cursor.count() > 0:
            return cursor.next()
        self.cadastraNovoAdversario(jogo)
        return self.__dict__

    def cadastraNovoAdversario(self,jogo):
        ident = Utils().proxIdent("Adversarios")
        self.nome = jogo.adversario
        self.ident = ident
        self.toMongo()


    def toMongo(self):
        Database().add(self, "Adversarios")