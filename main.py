__author__ = 'Felipe'
import codecs
codecs.BOM_UTF8
from Utils import Utils
from Jogador import *
from Adversario import *
from dbmongo import Database
from Relatorios import *

filename = "meusjogos.txt"
txt = codecs.open(filename, encoding="utf-8-sig")
todosjogos = txt.readlines()

def main():
    for linhajogo in todosjogos :
        jogo = Utils().parserJogos(linhajogo)
        ret = jogo.jogoExiste()
        if ret:
            print str(jogo.ident) + " - New Game  Inserted!"
            cadastraJogadores(jogo)
            Adversario().cadastraAdversarios(jogo)
            jogo.toMongo()
        else:
            print str(jogo.ident) + " Old Game - Not inserted"

    Relatorio().criaRelatorioMaisJogos()
    Relatorio().criaRelatorioMaisGols()
    Relatorio().criaRelatorioEstatisticas()
    Relatorio().criaRelatorioAdversarios()

def cadastraJogadores(jogo):
    for titular in jogo.titulares:
        jogador = jogadorExiste(titular, jogo.ano)
        atualizaNumeroDeJogos(jogador, "titular")
    for reserva in jogo.reservas:
        jogador = jogadorExiste(reserva, jogo.ano)
        atualizaNumeroDeJogos(jogador, "reserva")
    for gol in jogo.gols:
        jogador = jogadorExiste(gol, jogo.ano)
        atualizaNumeroDeGols(jogador)

def atualizaNumeroDeGols(jogador):
    jogador["gols"] = jogador["gols"] + 1
    Database().updatedata({"ident":jogador["ident"]}, jogador, "Jogadores")

def atualizaNumeroDeJogos(jogador, titularOuReserva):
    jogador[titularOuReserva] = jogador[titularOuReserva] + 1
    jogador["totalJogos"]     = jogador["totalJogos"] + 1
    Database().updatedata({"ident":jogador["ident"]}, jogador, "Jogadores")

def jogadorExiste(nome, anoJogo):
    jsonQuery = {'nome':nome}
    cursor = Database().getdata(jsonQuery,0,"Jogadores")
    if cursor.count() > 0:
        for jogador in cursor:
            for ano in jogador["anos"]:
                if ano == anoJogo:
                    return jogador
    jogador = cadastraNovoJogador(nome,anoJogo)
    return jogador

def cadastraNovoJogador(nome,ano):
    jogador = Jogador()
    jogador.nome = nome
    jogador.anos.append(ano)
    jogador.ident = Utils().proxIdent("Jogadores")
    posicao = str(raw_input("Qual posicao do jogador "+nome+" do Ano de "+str(ano)))
    jogador.posicao = posicao.upper()

    jsonQuery = {'nome':nome,'posicao':jogador.posicao}
    cursor = Database().getdata(jsonQuery,0,"Jogadores")
    if cursor.count() > 0:
        for jog in cursor:
            jog["anos"].append(ano)
            Database().updatedata({"ident":jog["ident"]}, jog, "Jogadores")
            return jog
    else:
        Database().add(jogador,"Jogadores")
    return jogador.__dict__

main()