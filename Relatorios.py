__author__ = 'Felipe'
import pymongo
from dbmongo import *

class Relatorio:
    def criaRelatorioMaisJogos(self):
        filename = "Stats_MaisJogos.txt"
        file = open(filename, 'w')
        query = {}
        sortby = [("totalJogos",pymongo.DESCENDING)]
        cursorJogadores = Database().getdata(query=query, sortby=sortby, collection="Jogadores")
        for jogador in cursorJogadores:
            file.write(jogador["nome"].ljust(25) + " - " + str(int(jogador["totalJogos"])).rjust(3) + " jogos(" + str(jogador["titular"]).rjust(3) +" titular)\r\n")

    def criaRelatorioMaisGols(self):
        filename = "Stats_MaisGols.txt"
        file = open(filename, 'w')
        query = {}
        sortby = [("gols",pymongo.DESCENDING)]
        cursorJogadores = Database().getdata(query=query, sortby=sortby, collection="Jogadores")
        totalDeGols = 0
        for jogador in cursorJogadores:
            if jogador["gols"] > 0:
                if jogador["nome"] != "CONTRA":
                    media = float(jogador["gols"])/float(jogador["totalJogos"])
                    media = format(round(media,2))
                else:
                    media = 0
                totalDeGols += jogador["gols"]
                file.write(jogador["nome"].ljust(25) + " - " + str(jogador["gols"]).rjust(2) + " Gols em " + str(jogador["totalJogos"]).rjust(3) + "jogos(" + str(jogador["titular"]).rjust(3) + " titular) - " + str(media).ljust(4) + " p/jogo\r\n")
        file.write("\r\nTOTAL DE GOLS: "+ str(totalDeGols))

    def criaRelatorioAdversarios(self):
        filename = "Stats_Adversarios.txt"
        file = open(filename, 'w')
        query = {}
        sortby = [("jogos",pymongo.DESCENDING)]
        cursorAdversarios = Database().getdata(query=query, sortby=sortby, collection="Adversarios")
        totalDeGols = 0
        for adversario in cursorAdversarios:
            totalDeGols = totalDeGols + adversario["golsFeitos"]
            file.write(adversario["nome"].ljust(25) + " - " + str(adversario["jogos"]).rjust(2) + " Jogos   "
                                                            + str(adversario["vitorias"]).rjust(2) + " V   "
                                                            + str(adversario["empates"]).rjust(2)  + " E   "
                                                            + str(adversario["derrotas"]).rjust(2) + " D   "
                                                            + str(adversario["golsFeitos"]).rjust(3)    + " Gols Feitos  "
                                                            + str(adversario["golsSofridos"]).rjust(3)  + " Gols Sofridos  " + " \r\n")
        file.write("\r\nTOTAL DE GOLS: "+ str(totalDeGols))

    def criaRelatorioEstatisticas(self):
        statsAno = []
        filename = "Stats.txt"
        file = open(filename, 'w')
        statGeral = EstatisticaBasica()
        statMineirao = EstatisticaBasica()
        statIndep = EstatisticaBasica()
        self.geraEstatisticas({}, statGeral)
        self.geraEstatisticas({"estadio":"MINEIRAO"}, statMineirao)
        self.geraEstatisticas({"estadio":"INDEPENDENCIA"}, statIndep)

        statTemp = EstatisticaBasica()
        for ano in range(1995, datetime.now().year+1, 1):
            if self.geraEstatisticas({"ano":ano}, statTemp):
                statTemp.ano = ano
                statsAno.append(statTemp)
                statTemp = EstatisticaBasica()


        self.escreveArquivoEstatisticasGerais(statGeral,    "GERAL:",         file)
        self.escreveArquivoEstatisticasGerais(statMineirao, "Mineirao:",      file)
        self.escreveArquivoEstatisticasGerais(statIndep,    "Independencia:", file)

        file.write("Estatisticas Por Ano:\r\n")
        for stat in statsAno:
            self.escreveArquivoEstatisticasAno(stat,    str(stat.ano)+": ",         file)

    def geraEstatisticas(self, query, stat):
        cursorJogos = Database().getdata(query=query, sortby=0, collection="Jogos")
        if cursorJogos.count() == 0:
            return False
        for jogo in cursorJogos:
            self.calculaEstatistica(jogo, stat)
        stat.calculaAproveitamento()
        stat.calculaMediaPublico()
        return True

    def calculaEstatistica(self, jogo, stat):
        if int(jogo["placarCruzeiro"]) > int(jogo["placarAdv"]):
            stat.vitorias += 1
        elif int(jogo["placarCruzeiro"]) == int(jogo["placarAdv"]):
            stat.empates += 1
        else:
            stat.derrotas += 1
        stat.jogos += 1
        stat.golsFeitos += int(jogo["placarCruzeiro"])
        stat.golsSofridos += int(jogo["placarAdv"])
        stat.publicoTotal += int(jogo["publico"])

    def escreveArquivoEstatisticasGerais(self, stat, titulo, file):
        file.write(titulo+"\r\n")
        file.write(str(stat.jogos).rjust(7)    + " jogos "       + "\r\n")
        file.write(str(stat.vitorias).rjust(7) + " vitorias "    + "\r\n")
        file.write(str(stat.empates).rjust(7)  + " empates "     + "\r\n")
        file.write(str(stat.derrotas).rjust(7) + " derrotas "    + "\r\n")
        aprov = format(round((stat.aproveitamento),1))
        file.write(str(aprov).rjust(6) + "% aproveitamento "    + "\r\n")
        file.write(str(stat.golsFeitos).rjust(7)   + " gols feitos "   + "\r\n")
        file.write(str(stat.golsSofridos).rjust(7) + " gols sofridos " + "\r\n")
        file.write(str(int(round(stat.mediaPublico,0))).rjust(7)   + " pagantes "   + "\r\n\r\n\r\n")

    def escreveArquivoEstatisticasAno(self, stat, titulo, file):
        file.write(titulo+" ")
        file.write(str(stat.jogos).rjust(3)    + "j ")
        file.write(str(stat.vitorias).rjust(3) + "v ")
        file.write(str(stat.empates).rjust(3)  + "e ")
        file.write(str(stat.derrotas).rjust(3) + "d ")
        aprov = format(round((stat.aproveitamento),1))
        file.write(str(aprov).rjust(8) + "% aprov. ")
        file.write(str(stat.golsFeitos).rjust(5)   + " gols feitos ")
        file.write(str(stat.golsSofridos).rjust(5) + " gols sofridos ")
        file.write(str(int(round(stat.mediaPublico,0))).rjust(8)   + " pagantes "+ "\r\n")

class EstatisticaBasica:
        def __init__(self):
            self.ano = 0
            self.jogos = 0
            self.vitorias = 0
            self.empates = 0
            self.derrotas = 0
            self.aproveitamento = 0
            self.publicoTotal = 0
            self.mediaPublico = 0
            self.golsFeitos = 0
            self.golsSofridos = 0

        def calculaAproveitamento(self):
            maxPontos = self.jogos * 3
            pontos = (self.vitorias*3) + self.empates
            self.aproveitamento = (float(pontos)/float(maxPontos))*100

        def calculaMediaPublico(self):
            self.mediaPublico = float(self.publicoTotal)/float(self.jogos)

