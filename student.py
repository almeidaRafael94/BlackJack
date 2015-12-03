# encoding: utf8
__author__ = 'Rafael Almeida 68486'
__email__ = 'almeidarafael@ua.pt'

__author__ = 'João Quintanilha 68065'
__email__ = 'jpquintanilha@ua.pt'

__author__ = 'Fábio Costa 68767'
__email__ = 'f.costa999@ua.pt'

__version__ = "0.1"
import card
import random
from player import Player


class StudentPlayer(Player):
    def __init__(self, name="Student", money=0):
        super(StudentPlayer, self).__init__(name, money)
        self.initial_money = money
        self.value_cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  # cards value
        self.dealer_cards = 0
        self.firstBet = True;
        self.winCount = 0
        self.loseCount = 0
        self.minBet = 0
        self.maxBet = 0
        self.countCondWin = 0
        self.countCondLose = 0
        self.cond = False
        self.countSurrender = 0

        # controlo de 
        self.banca = 0
        self.done = False
        self.valueToPlay = 0


    def play(self, dealer, players):

        player = [x for x in players if x.player.name == self.name][0]  # player = my boot (name = Student)
        dealer_value = card.value(dealer.hand) if card.value(dealer.hand) <= 21 else 0  # value cards dealer
        player_value = card.value(player.hand) if card.value(player.hand) <= 21 else 0  # value cards my boot

        if (self.firstBet):
            op = self.firstMove(player, dealer, player_value, dealer_value)
            self.firstBet = False;
        else:
            op = self.moderatePlayer(player, dealer, player_value, dealer_value)

        self.dealer_cards = len(dealer.hand)

        return op


    def bet(self, dealer, players):

        self.firstBet = True

        # strtmp = readFile("pocket.txt")                                       # para criação do gráfico POCKET/NJogadas
        # strtmp += str(self.pocket)
        # writeFile(strtmp,"pocket.txt")

        attitude = self.aggressivity_power(self.pocket, self.initial_money)  # apostar percentagem de popcket

        #apostar percentagem de pocket
        '''
        if (attitude == "aggressive"):
            bet = self.pocket * 0.1000
        elif (attitude == "moderateUp"):
            bet = self.pocket * 0.0600
        elif (attitude == "moderateDown"):
            bet = self.pocket * 0.0400
        else:
            bet = self.pocket * 0.0200
        '''

        #apostar percentagem de valor para jogar
        if (attitude == "aggressive"):
            bet = self.valueToPlay * 0.1000
        elif (attitude == "moderateUp"):
            bet = self.valueToPlay * 0.0600
        elif (attitude == "moderateDown"):
            bet = self.valueToPlay * 0.0400
        else:
            bet = self.valueToPlay * 0.0200

        bet = int(round(bet))
        # reduzir a perda caso aconteça
        if(bet >= self.valueToPlay):        # Reduzir a probabilidade de ficar com dinheiro negativo
            bet = self.valueToPlay

        if (bet < self.minBet):
            bet = self.minBet
        if (bet > self.maxBet):
            bet = self.maxBet

        if(bet % 2 != 0):               # garantir o retorno inteiro no caso de op = "u"
           bet = bet +1

        return bet

    def payback(self, prize):

        #strtmp = self.readFile("values.txt")

        if (prize > 0):
            self.winCount += 1
            #strtmp += "\nWIN!"
        if (prize < 0):
            self.loseCount += 1
            #strtmp += "\nLOSE!"

        #self.writeFile(strtmp, "values.txt")

        super(StudentPlayer, self).payback(prize)
        self.dealer_cards = 0

        #print "\nWINS COUNTER = %(first)d | LOSE COUNTER = %(second)d" % {"first": self.winCount,
        #                                                                  "second": self.loseCount}
        if (self.cond):
            if (prize > 0):
                self.countCondWin += 1
            elif (prize < 0):
                self.countCondLose += 1
        self.cond = False
        #print "\nWIN COUNTER COND = %(first)d | LOSE COUNTER COND= %(second)d" % {"first": self.countCondWin,"second": self.countCondLose}
        #print "\n nr de surrenders " + str(self.countSurrender)

#-------------------------------------------- PLAYER PROBS -------------------------------------------#
    def player_probability(self, player):  # return [prob_not_bust,prob_bust]


        player_value = card.value(player.hand) if card.value(player.hand) <= 21 else 0  # value cards my boot

        player_hand_Ace = False  # mao do player contem Ace
        player_hand_nAce = 0  # numero de Ace's visiveis do player
        if any(c.is_ace() for c in player.hand):
            player_hand_Ace = True
        for c in player.hand:
            if c.is_ace():
                player_hand_nAce += 1;

        player_totalValue = 0  # valor total da mao do player

        for c in player.hand:
            if c.is_ace():
                player_totalValue += c.value() + 10
            else:
                player_totalValue += c.value()
                # CASO PLAYER FACA HIT
        dif_player = 0
        # diferenca entre blackjack e o valor da mao do dealer
        if (player_hand_Ace):  # Caso a mao do dealer contenha 1 ou mais Ace's
            if (player_value != player_totalValue):
                dif_player = 21 - player_value  # teremos que subtratir o o numero de Ace * 10
            else:
                dif_player = 21 - (
                    player_totalValue - (player_hand_nAce * 10))
        else:
            dif_player = 21 - player_value;

        num_benefit_cards_player = len(
            [x for x in self.value_cards if dif_player >= x])  # numer de cartas beneficas para o player
        prob_player_not_bust = 1.0 * num_benefit_cards_player / 13  # probabilidade de player melhorar a sua mao
        prob_player_bust = 1 - (1.0 * prob_player_not_bust)  # probabilidade de o player fazer bust

        if (player_hand_Ace):  # calcular probabilidade de melhorar mao em caso de "h"
            prob_better_hand = 1.0 * (21 - player_value) / 13
        else:
            prob_better_hand = prob_player_not_bust

        return [prob_player_bust, prob_better_hand]


#-------------------------------------------- DEALER PROBS -------------------------------------------#
    def dealer_probability(self, dealer):

        dealer_value = card.value(dealer.hand) if card.value(dealer.hand) <= 21 else 0  # value cards dealer
        dealer_value_estimated = dealer_value + 6.85  # valor estimado da mao do delaer

        # print "dealer_value = " +str(dealer_value)

        dealer_hand_Ace = False  # mao do dealer contem Ace
        dealer_hand_nAce = 0  # numero de Ace's visiveis do dealer
        if any(c.is_ace() for c in dealer.hand):
            dealer_hand_Ace = True
        for c in dealer.hand:
            if c.is_ace():
                dealer_hand_nAce += 1;

        # print "\ndealer_hand_Ace : %s" % str(dealer_hand_Ace)
        # print "\ndealer_hand_nAce: %s" % str(dealer_hand_nAce)

        dealer_totalValue = 0  # valor total da mao do delaer
        dealer_totalValue_estimated = 0  # valoer total estimado da mao do dealer

        for c in dealer.hand:
            if c.is_ace():
                dealer_totalValue += c.value() + 10
            else:
                dealer_totalValue += c.value()

        dealer_totalValue_estimated = dealer_totalValue + 6.85

        # print "\ndealer_totalValue: %d" % dealer_totalValue
        # print "\ndealer_totalValue_estimated: %d" % dealer_totalValue_estimated


        dif_dealer = 0
        dif_dealer_estimated = 0

        if (dealer_hand_Ace):  # diferenca entre blackjack e o valor da mao do dealer
            if (dealer_value != dealer_totalValue):  # Caso a mao do dealer contenha 1 ou mais Ace's
                dif_dealer = 21 - dealer_value
            else:
                dif_dealer = 21 - (
                    dealer_totalValue - (dealer_hand_nAce * 10))  # teremos que subtratir o o numero de Ace * 10
        else:
            dif_dealer = 21 - dealer_value

        dif_dealer_estimated = (dif_dealer - 6.85) + 1

        # print "\ndif_dealer: %d" % dif_dealer
        # print "\ndif_dealer_estimated: %d" % dif_dealer_estimated

        num_benefit_cards_dealer = len(
            [x for x in self.value_cards if dif_dealer >= x])  # numer de cartas beneficas para o dealer

        num_benefit_cards_dealer_estimated = len(
            [x for x in self.value_cards if dif_dealer_estimated >= x])

        # print "\nnum_benefit_cards_dealer: %d" % num_benefit_cards_dealer
        # print "\nnum_benefit_cards_dealer_estimated: %d" % num_benefit_cards_dealer_estimated

        prob_dealer_not_bust = 1.0 * num_benefit_cards_dealer / 13  # probabilidade de dealer melhorar a sua mao
        prob_dealer_bust = 1 - (1.0 * prob_dealer_not_bust)
        prob_dealer_not_bust_estimated = 1.0 * num_benefit_cards_dealer_estimated / 13
        prob_dealer_bust_estimated = 1 - (1.0 * prob_dealer_not_bust_estimated)

        if (dealer_hand_Ace):  # calcular probabilidade de melhorar mao
            prob_better_hand = 1.0 * (21 - dealer_value) / 13
            prob_better_hand_estimated = 1.0 * (21 - dealer_value_estimated) / 13
        else:
            prob_better_hand = prob_dealer_not_bust
            prob_better_hand_estimated = prob_dealer_not_bust_estimated

        count = 0
        for c in self.value_cards:
            if (c < (17 - dealer_value)):
                count += 1

        if (dealer_value < 17):  # probabilidade do dealer fazer hit na proxima jogada
            if (dealer_value <= 10):
                if (count > 12):
                    count = 12;
                prob_hit = 1.0 * (count + 1) / 13  # +1 porque o Ace é favorável neste caso
            else:
                prob_hit = 1.0 * (count) / 13
        else:
            prob_hit = 0

        countEstimated = 0
        for c in self.value_cards:
            if (c < (17 - dealer_value_estimated)):
                countEstimated += 1

        if (dealer_value_estimated < 17):  # probabilidade estimada
            # do dealer fazer hit na proxima jogada
            if (dealer_value_estimated <= 10):
                if (countEstimated > 12):
                    countEstimated = 12;
                prob_hit_estimated = 1.0 * (countEstimated + 1) / 13  # +1 porque o Ace é favorável neste caso
            else:
                prob_hit_estimated = 1.0 * (countEstimated) / 13
        else:
            prob_hit_estimated = 0

        return [prob_dealer_bust, prob_better_hand, prob_hit,
                prob_dealer_bust_estimated, prob_better_hand_estimated, prob_hit_estimated]


#-------------------------------------------- FIRST MOVE -------------------------------------------#
    def firstMove(self, player, dealer, player_value, dealer_value):
        #strtmp = self.readFile("values.txt")
        if(dealer_value+11 < 17):
            if(player_value == 10 or player_value == 11):
                op = "d"
            else:
                op = "s"
                #strtmp += str("\nÉ a primeira jogada! Max_dealer_value < 17 \nOP -> s")

            #SE O JOGADOR TEM MAO SOFT
        elif self.playerHasAce(player) == True:
            #strtmp += str("\nÉ a primeira jogada, e o Jogador tem um A's na mao")
            if dealer_value == 6 or dealer_value == 7 or dealer_value == 8 or dealer_value ==11:
            	if player_value >= 18:
            		op="s"
            		#strtmp += str("\nPlayer value >= 18 e o dealer == 6, 7, 8 ou 11\nOP -> s")
            	else:
            		op="h"
            		#strtmp += str("\nPlayer value < 18 e o dealer == 6, 7, 8 ou 11\nOP -> h")
            else:
            	if player_value >= 19:
            		op="s"
            		#strtmp += str("\nPlayer value >= 19 e o dealer == 9 ou 10\nOP -> s")
            	else:
            		op="h"
            		#strtmp += str("\nPlayer value < 19 e o dealer == 9 ou 10\nOP -> h")


            #SE O JOGADOR NAO TEM MAO SOFT
        else:
            #strtmp += str("É a primeira jogada, e o Jogador não tem um A's na mao")
            if dealer_value == 6:
            	if player_value >= 12:
            		op="s"
            		#strtmp += str("\nPlayer value >= 12 e o dealer == 6\nOP -> s")
            	elif (player_value == 9 or player_value == 10 or player_value == 11):
            		op = "d"
            		#strtmp += str("\n 8 < Player value < 12 e o dealer == 6\nOP -> d")
            	else:
            		op="h"
            		#strtmp += str("\nPlayer value < 12 e o dealer == 6\nOP -> h")

            elif (dealer_value == 7 or dealer_value == 8 or dealer_value == 9):
            	if player_value == 10 or player_value == 11:
            		op = "d"
            		#strtmp += str("\nPlayer value == 10 ou 11 e o dealer == 7, 8 ou 9\nOP -> d")
            	elif player_value>=17:
            		op = "s"
            		#strtmp += str("\nPlayer value >= 17 e o dealer == 7, 8 ou 9\nOP -> s")
            	else:
            		op = "h"
            		#strtmp += str("\nPlayer value < 17, != 10 ou 11 e o dealer == 7, 8 ou 9\nOP -> h")
            else:
            	if player_value>=17:
            		op="s"
            		#strtmp += str("\nPlayer value >= 17 e o dealer > 6\nOP -> s")
                elif(player_value >= 15):
                    op = "u"
            	else:
            		op="h"
            		#strtmp += str("\nPlayer value < 17 e o dealer > 6\nOP -> h")

        #self.writeFile(strtmp,"values.txt")

        return op


#-------------------------------------------- MODERATE PLAYER -------------------------------------------#
    def moderatePlayer(self, player, dealer, player_value, dealer_value):  # player com atitude moderada

        player_probs = self.player_probability(player)
        player_prob_bust = player_probs[0]
        player_prob_not_bust = 1 - player_prob_bust
        player_prob_better_hand = player_probs[1]

        dealer_probs = self.dealer_probability(dealer)
        dealer_prob_bust = dealer_probs[0]
        dealer_prob_not_bust = 1 - dealer_prob_bust
        dealer_prob_better_hand = dealer_probs[1]
        dealer_prob_hit = dealer_probs[2]
        dealer_value_estimate = dealer_value + 6.85  # valor medio das cartas existentes ~ 6.85
        dealer_prob_bust_estimated = dealer_probs[3]
        dealer_prob_not_bust_estimated = 1 - dealer_prob_bust_estimated
        dealer_prob_better_hand_estimated = dealer_probs[4]
        dealer_prob_hit_estimated = dealer_probs[5]
        '''
        strtmp = self.readFile("values.txt")

        strtmp += "\nPlayer_value: " + str(player_value)
        strtmp += "\nPlayer_Bust: " + str(player_prob_bust)
        strtmp += "\nPlayer_NOT_BUST: " + str(player_prob_not_bust)
        strtmp += "\nPlayer_better_hand: " + str(player_prob_better_hand)
        # DEALER
        strtmp += "\nDealer_value: " + str(dealer_value)
        strtmp += "\nDealer_Bust: " + str(dealer_prob_bust)
        strtmp += "\nDealer_NOT_BUST: " + str(dealer_prob_not_bust)
        strtmp += "\nDealer_better_hand: " + str(dealer_prob_better_hand)
        strtmp += "\nDealer_prob_hit: " + str(dealer_prob_hit)
        # DEALER ESTIMATED
        strtmp += "\nDealer_value_estimated: " + str(dealer_value_estimate)
        strtmp += "\nDealer_Bust_estimated: " + str(dealer_prob_bust_estimated)
        strtmp += "\nDealer_NOT_BUST_estimated: " + str(dealer_prob_not_bust_estimated)
        strtmp += "\nDealer_better_hand_estimated: " + str(dealer_prob_better_hand_estimated)
        strtmp += "\nDealer_prob_hit_estimated: " + str(dealer_prob_hit_estimated)
        '''
        if (len(dealer.hand) > self.dealer_cards):  # valor da mao do dealer da ultima jogada
            last_dealer_value = "hit"
        else:
            last_dealer_value = "stand"

        #strtmp += "\nDealer_last_move  actual-> " + str(len(dealer.hand)) + " passada-> " + str(self.dealer_cards) + " move-> " + last_dealer_value
        self.dealer_cards = len(dealer.hand)

        # Valores de probabilidades disponiveis:

        # Player:
        # player_prob_bust          -> probabilidade do player, ao fazer hit, passar os 21 pontos
        # player_prob_not_bust      -> probabilidade do player, ao fazer hit, nao passar os 21 pontos
        # player_prob_better_hand   -> probabilidade do player fazer hit e melhorar a sua mao

        # Dealer:
        # dealer_prob_bust          -> probabilidade do dealer ter passado os 21 pontos tendo em conta a carta oculta
        # dealer_prob_not_bust      -> probabilidade do dealer nao ter passado os 21 pontos tendo em conta a carta oculta
        # dealer_prob_better_hand   -> probabilidade do dealer melhorar a sua mao tento em conta a carta oculta
        # dealer_prob_hit           -> probabilidade de dealer fazer hit na proxima jogada tendo em conta a carta oculta

        #--------------------- CONDITIONS ---------------_#

        op = ""

        cmd = ["h", "u"]
        cmd1 = ["s","u"]

        if(dealer_value < 6):                         # impossivel ter 17 ou mais
            op = "s"
        elif(player_value <= 11):                         # impossivel fazer bust
            op = "h"


        elif(last_dealer_value == "hit"):                   # delaer deu "hit"
            if(self.dealerHasAce(dealer)):
                if(player_value< 15):
                    op = "h"
                else:
                    op = "s"
            else:                                                # caso de bust impossível mas possivel 17+
                if(dealer_value >= 6 and dealer_value <= 11):
                    if dealer_value  == 6:
                        op = self.firstMove(player,dealer,player_value,dealer_value)
                        if op == "d":
                            op ="h"
                    elif dealer_value < 9:
                        op = self.firstMove(player,dealer,player_value,dealer_value)
                        if op == "d":
                            op = "h"
                    elif (dealer_value == 9 or dealer_value == 11):
                        if player_value == 16:
                            op = "u"
                            self.countSurrender+=1
                        elif player_value > 16:
                            op = "s"
                        else:
                            op = "h"
                    else:
                        if (player_value == 16 or player_value == 15):
                            op = "u"
                            self.countSurrender+=1
                        elif player_value > 16:
                            op = "s"
                        else:
                            op = "h"
                else:                                           # caso de possivel 17+ e possivel bust
                    if(dealer_value < 15):                      # dealer value ]11;15[
                        if(player_value <= 15):
                            op = "h"
                        else:
                            op = "s"
                    elif(dealer_value == 15):
                        if(player_value <= 13):
                            op = "h"
                        else:
                            op = "s"
                    elif(dealer_value >= 18):
                        op = "s"
                    else:
                        if(player_value < 13):
                            op = "h"
                        else:
                            op = "s"

        elif(last_dealer_value == "stand"):             # dealer já tem 17+
            if(self.dealerHasAce(dealer)):
                if(player_value < 14):
                    op = "h"
                elif(player_value == 4):
                    op = cmd[random.randint(0,1)]
                elif(player_value >= 17):
                    op = "s"
                else:
                    op = "u"
            else:
                if(dealer_value < 9):                       # dealer tem 17 , 18 ou 19
                    if(dealer_value == 6):
                        if(player_value <= 14):
                            op = "h"
                        elif(player_value < 17):
                            op = "u"
                        else:
                            op = "s"
                    elif(dealer_value == 8):
                        if(player_value < 14):
                            op = "h"
                        elif(player_value < 18):
                            op = "u"
                        else:
                            op = "s"
                    else:
                        if(player_value < 14):
                            op = "h"
                        elif(player_value < 18):
                            op = cmd1[random.randint(0,1)]
                        else:
                            op = "s"

                elif(dealer_value == 9 or dealer_value == 11):
                    if(player_value < 16):
                        op = "h"
                    elif(player_value == 16):
                        op = "u"
                        self.countSurrender+=1
                    else:
                        op = "s"
                elif(dealer_value == 10):
                    if(player_value < 15):
                        op = "h"
                    elif(player_value < 17):
                        op = "u"
                        self.countSurrender+=1
                    else:
                        op = "s"
                elif(dealer_value <= 14):
                    if(player_value <= 15):
                        op = "h"
                    elif(player_value == 16):
                        op = "u"
                        self.countSurrender+=1
                    else:
                        op = "s"
                elif(dealer_value == 15):
                    if(player_value < 15):
                        op = "h"
                    else:
                        op = "s"
                else:
                    if(player_value <= 13):
                        op = "h"
                    else:
                        op = "s"


        #strtmp += "\nOP -> " + op
        #self.writeFile(strtmp, "values.txt")
        return op

    def playerHasAce(self,player):
        for c in player.hand:
            if c.is_ace():
                return True
        return False

    def dealerHasAce(self,dealer):
        for c in dealer.hand:
            if c.is_ace():
                return True
        return False

    def writeFile(self, val, fileName):  # guarda info de jogadas no ficheiro
        fileobj = open(fileName, "w")
        fileobj.write(str(val) + '\n')
        fileobj.close()

    def readFile(self, fileName):  # lê info de jogadas no ficheiro
        fileobj = open(fileName, "r")
        info = fileobj.read()
        fileobj.close()
        return info

    def aggressivity_power(self, pocket, initial_money):  # Grau de agressividade da jogada
        # influencia:
        attitude = ""
        if (pocket >= initial_money + initial_money * 0.12):  # atitude do jogador
            attitude = "aggressive"
        elif (pocket <= initial_money + initial_money * 0.05):  # aposta de jogada
            attitude = "defensive"  # atitude agressiva implica aposta mais elevada
        elif (pocket > initial_money + initial_money * 0.1 and pocket < initial_money + initial_money * 0.12):
            attitude = "moderateUp"
        elif (pocket > initial_money + initial_money * 0.05 and pocket <= initial_money + initial_money * 0.1):
            attitude = "moderateDown"
        else:
            attitude = "defensive"

        return attitude

    def want_to_play(self, rules):   #overwrite
        self.minBet = rules.min_bet
        self.maxBet = rules.max_bet


        if(self.done):                                                  # já não joga mais
            return False

        # Decidir com que valor pode jogar de forma a minimizar/anular a perda

        if(self.pocket > self.initial_money):
            print "POCKET > INICIAL"
            if(self.valueToPlay >= self.initial_money * 1.20):
                print "VALUE > INICIAL*1.2"
                self.banca += self.initial_money*0.20
                self.valueToPlay -= self.initial_money*0.20
            elif(self.banca == 0):
                print "VALUE <  INICIAL*1.2 , BANCA == 0"
                self.valueToPlay = self.pocket
            else:
                print "VALUE <  INICIAL*1.2 , BANCA > 0"
                if(self.pocket < self.valueToPlay):
                    self.valueToPlay = self.pocket
                else:
                    self.valueToPlay = self.pocket-self.banca
        else:
            print "POCKET <= INICIAL"
            if(self.banca == 0):
                self.valueToPlay = self.pocket
            else:
                self.valueToPlay = self.pocket - self.banca

        print "POCKET: " + str(self.pocket) + " BANCA: " + str(self.banca) + " VALUE TO PLAY: " + str(self.valueToPlay)

        if(self.valueToPlay <= 0):                                      # se não tem dinheiro para apostar não joga mais
           self.done = True
           return False


        return True

