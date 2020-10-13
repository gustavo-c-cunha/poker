# INE 5404-02208A - POO II
# Gustavo Cunha e Felipe Goulart
# coding: utf-8

import random
from treys import *

deck = Deck()
comparador = Evaluator()

class Jogador():
    def __init__(self, nome, fichas):
        self.nome = nome
        self.fichas = fichas
        self.fichasRodada = 0
        self.cartas = deck.draw(2)
        self.dealer = False
        self.sequencia = []
        self.status = True
        self.pontuacao = 0
        self.classe = ""
        self.sequencia = ""

    def calculaPontuacao(self):
        self.pontuacao = comparador.evaluate(mesa.cartas, self.cartas)
        self.classe = comparador.get_rank_class(self.pontuacao)
        self.sequencia = comparador.class_to_string(self.classe)

    def getNome(self):
        return self.nome

    def setNome(self, nNome):
        self.nome = nNome

    def apostaInicial(self, rodada):

        if self.status and self.fichasRodada != rodada.valor:
            print(self.getNome(), "deseja pagar", (rodada.valor - self.fichasRodada), "fichas?")
            resposta = input()
            resposta = resposta.lower()

            if resposta == "pagar" or resposta == "sim":
                print(self.nome, "pagou a aposta")
                print()
                self.fichas -= (rodada.valor - self.fichasRodada)
                self.fichasRodada += (rodada.valor - self.fichasRodada)
                

            elif resposta == "aumentar":
                v = int(input("Quantas fichas a mais? "))
                rodada.setValor(rodada.valor + v)

                print(self.nome, "aumentou o valor da aposta para", rodada.valor, "fichas")
                print()
                self.fichas -= (rodada.valor - self.fichasRodada)
                self.fichasRodada += (rodada.valor - self.fichasRodada)
            

            else:
                self.status = False
                rodada.excluirJogador(self)
                print(self.nome, "correu")
                print()

    def aposta(self, rodada):
        if self.status and rodada.valor == 0:
            print(self.getNome(), "deseja apostar?")
            resposta = input()
            resposta = resposta.lower()

            if resposta == "aumentar" or resposta == "sim":
                v = int(input("Quantas fichas? "))
                rodada.setValor(rodada.valor + v)

                print(self.nome, "apostou", rodada.valor, "fichas")
                print()
                self.fichas -= (rodada.valor - self.fichasRodada)
                self.fichasRodada += (rodada.valor - self.fichasRodada)
                

            elif resposta == "correr":
                self.status = False
                rodada.excluirJogador(self)
                print(self.nome, "correu")
                print()

            else:
                print(self.nome, "passou a vez")
                print()
                pass

        elif self.status and self.fichasRodada != rodada.valor:
            print(self.nome, "deseja cobrir a aposta e pagar", (rodada.valor - self.fichasRodada), "fichas?")
            resposta = input()
            resposta = resposta.lower()

            if resposta == "pagar" or resposta == "sim":
                print(self.nome, "pagou a aposta")
                print()
                self.fichas -= (rodada.valor - self.fichasRodada)
                self.fichasRodada += (rodada.valor - self.fichasRodada)
                

            elif resposta == "aumentar":
                v = int(input("Quantas fichas a mais?"))
                rodada.setValor(rodada.valor + v)

                print(self.nome, "aumentou o valor da aposta para", rodada.valor, "fichas")
                print()
                self.fichas -= (rodada.valor - self.fichasRodada)
                self.fichasRodada += (rodada.valor - self.fichasRodada)
                

            elif resposta == "correr" or resposta == "nao":
                self.status = False
                rodada.excluirJogador(self)
                print(self.nome, "correu")
                print()

        

    def getFichas(self):
        return self.fichas

    def setFichas(self, nFichas):
        self.fichas = nFichas

    def resetFichasRodada(self):
        self.fichasRodada = 0

    def addFichasRodada(self, fichas):
        self.fichasRodada += fichas

    def getCartas(self):
        return str(self.cartas[0][0]) + " de " + self.cartas[0][1] + ", " + str(self.cartas[1][0]) + " de " + self.cartas[1][1]

    def addCartas(self, nCarta):
        self.cartas.append(nCarta)

    def resetCartas(self):
        self.cartas = []

    def setDealer(self):
        self.dealer = True
        print(self.nome, "é o Dealer \n")

    def smallBlind(self):
        self.fichas -= mesa.blind // 2
        print(self.nome, "pagou", (mesa.blind // 2), "fichas por Small Blind")
        self.fichasRodada += (mesa.blind // 2)

    def bigBlind(self):
        self.fichas -= mesa.blind
        print(self.nome, "pagou", (mesa.blind), "fichas por Big Blind")
        self.fichasRodada += (mesa.blind)
        
    
class Rodadas():

    def __init__(self, nome, valor, numero):
        self.nome = nome
        self.valor = valor
        self.status = True
        self.jogadores = []
        self.numero = numero

    def getValor(self):
        return self.valor

    def setValor(self, nValor):
        self.valor  = nValor

    def TerminaRodada(self):
        self.status = False

    def addJogador(self, jogador):
        self.jogadores.append(jogador)

    def excluirJogador(self, jogador):
        self.jogadores.remove(jogador)

    def iniciaRodada(self, rodadaAnterior):

        print()
        print("---- ", self.nome, "----")
        print()

        print("Fichas - Jogador")
        for i in range(0, len(rodadaAnterior.jogadores)):
            self.jogadores.append(rodadaAnterior.jogadores[i])
            print(self.jogadores[i].fichas, "  -", self.jogadores[i].nome)

        print()
        print("Cartas na Mesa:")
        for i in range(self.numero):
            print(Card.print_pretty_card(mesa.cartas[i]))
        print()

        


    def proximaRodada(self, proxRodada):

        if len(self.jogadores) == 1:
            print("---", self.jogadores[0].nome, "venceu! ---")
            print(self.jogadores[0].nome, "ganhou", mesa.valorAcumulado, "fichas!")
            print()

        else:

            for i in range(0, len(self.jogadores)):
                if self.jogadores[i].status:
                    if self.jogadores[i].fichasRodada != self.valor:
                        break
                        
                    if i == (len(self.jogadores) - 1):
                        self.status = False

                        for i in range(0, len(self.jogadores)):
                            mesa.addValorAcumulado(self.jogadores[i].fichasRodada)
                            self.jogadores[i].resetFichasRodada()

                        proxRodada.iniciaRodada(self)

            




class Mesa():

    def __init__(self):
        self.jogadores = []
        self.valorAcumulado = 0
        self.cartas = deck.draw(5)
        self.blind = 10
        self.valorAposta = self.blind

    def addFichas(self, fichas):
        self.valorAcumulado += fichas

    def addAposta(self, valor):
        self.valorAposta += valor

    def addValorAcumulado(self, valor):
        self.valorAcumulado += valor

    def getJogadores(self):
        return self.jogadores

    def addJogador(self, jogador):
        self.jogadores.append(jogador)

    def excluirJogador(self, jogador):
        self.jogadores.remove(jogador)

    def getCartas(self):
        return self.cartas

    def mostraCartas(self):
        print()
        print(Card.print_pretty_cards(j1.cartas), "-", j1.nome)
        print(Card.print_pretty_cards(j2.cartas), "-", j2.nome)
        print(Card.print_pretty_cards(j3.cartas), "-", j3.nome)
        print(Card.print_pretty_cards(j4.cartas), "-", j4.nome)
        print()




#Cria uma mesa
mesa = Mesa()

# Cria as rodadas
rodada1 = Rodadas("Pré Flop", mesa.blind, 0)
rodada2 = Rodadas("Flop", 0, 3)
rodada3 = Rodadas("Turn", 0, 4)
rodada4 = Rodadas("River", 0, 5)
rodada5 = Rodadas("Showdow", 0, 5)

# Cria os jogadores
j1 = Jogador("Gustavo", 1000)
mesa.addJogador(j1)

j2 = Jogador("Felipe", 1000)
mesa.addJogador(j2)

j3 = Jogador("Gabriel", 1000)
mesa.addJogador(j3)

j4 = Jogador("Alex", 1000)
mesa.addJogador(j4)


# Adicionando todos os jogadores a rodada 1
for i in range(len(mesa.jogadores)):
    rodada1.addJogador(mesa.jogadores[i])


# Definições Iniciais
print()
print("-- Texas Hold'em Poker -- \n")

print("Fichas - Jogador")
for i in range(len(mesa.jogadores)):
    print(mesa.jogadores[i].fichas, "  -", mesa.jogadores[i].nome)

print("------------------")

#Define o Dealer
j1.setDealer()
j2.smallBlind()
j3.bigBlind()


#Distribui as Cartas
mesa.mostraCartas()


#Loop principal
while True:

    #loop do pré flop

    print("---", rodada1.nome, "---")
    print()
    while rodada1.status:

        j4.apostaInicial(rodada1)

        j1.apostaInicial(rodada1)

        j2.apostaInicial(rodada1)

        j3.apostaInicial(rodada1)

        rodada1.proximaRodada(rodada2)


    
    while rodada2.status:


        j1.aposta(rodada2)

        j2.aposta(rodada2)

        j3.aposta(rodada2)

        j4.aposta(rodada2)

        rodada2.proximaRodada(rodada3)

    
    while rodada3.status:


        j1.aposta(rodada3)

        j2.aposta(rodada3)

        j3.aposta(rodada3)

        j4.aposta(rodada3)

        rodada3.proximaRodada(rodada4)


    while rodada4.status:

        j1.aposta(rodada4)

        j2.aposta(rodada4)

        j3.aposta(rodada4)

        j4.aposta(rodada4)

        rodada4.proximaRodada(rodada5)

    while rodada5.status:

        print("Valor total na mesa:", mesa.valorAcumulado, "fichas")

        menor = 9000
        vencedor = ''
        sequ = ''

        for i in range(len(rodada5.jogadores)):
            rodada5.jogadores[i].calculaPontuacao()
            
            if rodada5.jogadores[i].pontuacao < menor:
                menor = rodada5.jogadores[i].pontuacao
                vencedor = rodada5.jogadores[i].nome
                sequ = rodada5.jogadores[i].sequencia

            print(Card.print_pretty_cards(rodada5.jogadores[i].cartas), "-", rodada5.jogadores[i].nome)

        print()
        print("---", vencedor, "é o Vencedor com", sequ + "! ---")
        print("---", vencedor, "ganhou", mesa.valorAcumulado, "fichas! ---")
        print()

        a = input("Fim da Execução. Pressione enter para finalizar.")

        break
    break

        