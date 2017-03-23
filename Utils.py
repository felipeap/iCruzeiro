__author__ = 'Felipe'
from datetime import date, datetime
from Jogo import Jogo
from dbmongo import Database
import pymongo

class Utils:
    @staticmethod
    def paraMaiusculo(lista):
        l = [item.upper() for item in lista]
        return l

    @staticmethod
    def isInList(lista, newPos):
        for x in lista:
            if x == newPos:
                return True
        lista.append(newPos)
        lista.sort()
        return False

    def proxIdent(self, col):
        jsonQuery = {}
        sortby = [("ident",pymongo.DESCENDING)]
        cursor = Database().getdata(jsonQuery,sortby,col)
        if cursor.count() == 0:
            return 1
        else:
            for pos in cursor:
                return pos["ident"] + 1

    def parserJogos(self, linhajogo):
        linhaquebrada = linhajogo.split("-")
        jogoquebrado = linhaquebrada[0].split(",")
        titulares = linhaquebrada[1].split(",")
        reservas = linhaquebrada[2].split(",")
        tecnico = linhaquebrada[3]
        gols = linhaquebrada[4].split(",")

        jogoquebrado    = self.paraMaiusculo(jogoquebrado)
        titulares       = self.paraMaiusculo(titulares)
        reservas        = self.paraMaiusculo(reservas)
        tecnico         = tecnico.upper()
        gols            = self.paraMaiusculo(gols)
        gols[len(gols)-1] = gols[len(gols)-1].rstrip('\r\n')
        if gols[0] == '':
            gols = []
        if reservas[0] == '':
            reservas = []

        if len(titulares) != 11:
            print "Numero de Titulares errado - Jogo Numero: " + str(jogoquebrado[0])
            print titulares
        if len(reservas) > 3:
            print "Numero de Reservas errado - Jogo Numero: " + str(jogoquebrado[0])
            print reservas
        if len(gols) != int(jogoquebrado[6]):
            print "Numero de Gols errado - Jogo Numero: " + str(jogoquebrado[0])
            print gols
            print jogoquebrado[6]
        if tecnico == '':
            print jogoquebrado[0]
        #manipular data
        data = datetime.strptime(jogoquebrado[2], "%d/%m/%Y").date()
        jogo = Jogo(ident=int(jogoquebrado[0]),
                    estadio=jogoquebrado[1],
                    data=data,
                    publico=jogoquebrado[3],
                    renda=jogoquebrado[4],
                    campeonato=jogoquebrado[5],
                    placarCruzeiro=jogoquebrado[6],
                    placarAdv=jogoquebrado[7],
                    adversario=jogoquebrado[8],
                    titulares=titulares,
                    reservas=reservas,
                    tecnico=tecnico,
                    gols=gols,
                    ano=data.year)
        return jogo