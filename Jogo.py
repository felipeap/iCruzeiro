__author__ = 'Felipe'
from dbmongo import Database

class Jogo:
    def __init__(self,ident=0, estadio="", placarCruzeiro=0, placarAdv=0, adversario="", publico=0, renda=0, data=0, campeonato="",gols=[], titulares=[], reservas=[],tecnico="",ano=1989):
        self.ident = ident
        self.estadio = estadio
        self.placarCruzeiro = placarCruzeiro
        self.placarAdv = placarAdv
        self.adversario = adversario
        self.publico = publico
        self.data = data
        self.campeonato = campeonato
        self.renda = renda
        self.gols = gols
        self.titulares = titulares
        self.reservas = reservas
        self.tecnico = tecnico
        self.ano = ano

    def jogoExiste(self):
        query = {'ident':self.ident}
        col = "Jogos"
        cursor = Database().getdata(query=query, sortby=0, collection=col)
        if cursor.count() == 0:
            return True
        else:
            return False

    def toMongo(self):
        Database().add(self, "Jogos")