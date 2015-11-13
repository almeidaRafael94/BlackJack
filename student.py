#encoding: utf8
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
from collections import Counter

class StudentPlayer(Player):
    def __init__(self, name="Student", money=0):
        super(StudentPlayer, self).__init__(name, money)

    def play(self, dealer, players):

        player = [x for x in players if x.player.name == self.name][0]                   # player = my boot (name = Student)
        dealer_value = card.value(dealer.hand) if card.value(dealer.hand) <= 21 else 0   # value cards dealer
        player_value = card.value(player.hand) if card.value(player.hand) <= 21 else 0   # value cards my boot

        print "Dealer_Hand: [%s]" % str(dealer.hand)
        print "Dealer_value: %d" % dealer_value
        print "Player_Hand: [%s]" % player.hand
        print "Player_value: %d" % player_value

        print "++++++++++++PLAYER[not_bust , bust]+++++++++++++++++"
        print player_probability(self,player)
        print "++++++++++++DEALER[not_bust , bust]+++++++++++++++++"
        print dealer_probability(self,dealer)
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++"
        player_prob_bust = player_probability(self,player)[1]
        player_prob_not_bust = player_probability(self,player)[0]
        dealer_prob_bust = dealer_probability(self,dealer)[1]
        dealer_prob_not_bust = dealer_probability(self,dealer)[0]

        strtmp = readFile(self)
        strtmp += "\nPlayer_Bust "  + str(player_prob_bust)
        strtmp += "\nPlayer_NOT_BUST " + str(player_prob_not_bust)
        strtmp += "\nDealer_Bust "  + str(dealer_prob_bust)
        strtmp += "\nDealer_NOT_BUST " + str(dealer_prob_not_bust)

        op = ""
        if(player_value>16):
            op = "s"
        elif(dealer_prob_bust >= 0.80):
            op = "s"
        elif(dealer_prob_bust > 0.7 and dealer_prob_bust < 0.8):
            if(player_prob_bust >= 0.7):
                cmd = ["h", "s"]
                op = cmd[random.randint(0,1)]
            elif(player_prob_bust <= 0.3):
                op = "h"
            else:
                cmd = ["h","h", "h", "s"]
                op = cmd[random.randint(0,3)]

        elif(dealer_prob_bust > 0.4 and dealer_prob_bust < 0.7):
            if(player_prob_bust >= 0.6):
                cmd = ["h", "s", "s", "s"]
                op = cmd[random.randint(0,3)]
            elif(player_prob_bust <= 0.2):
                op = "h"
            else:
                cmd = ["h","s"]
                op = cmd[random.randint(0,1)]
        else:
            if(player_prob_bust >= 0.6):
                op = "s"
            elif(player_prob_bust <= 0.4):
                op = "h"
            else:
                cmd = ["h","s"]
                op = cmd[random.randint(0,1)]

        strtmp += "\nOP -> " + op
        writeVal_file(self,strtmp)
        return op



    def bet(self, dealer, players):
        cmd = [1]
        return cmd[random.randint(0,0)]

def player_probability(self,player):                                                # return [prob_not_bust,prob_bust]
    value_cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]                       # cards value
    player_value = card.value(player.hand) if card.value(player.hand) <= 21 else 0  # value cards my boot

    player_hand_Ace = False                                                          # mao do player contem Ace
    player_hand_nAce = 0                                                             # numero de Ace's visiveis do player
    if any(c.is_ace() for c in player.hand):
        player_hand_Ace =  True
    for c in player.hand:
        if c.is_ace():
            player_hand_nAce += 1;

    player_totalValue = 0                                                            # valor total da mao do player

    for c in player.hand:
        if c.is_ace():
            player_totalValue += c.value() + 10
        else:
            player_totalValue += c.value()
                                                                                       # CASO PLAYER FACA HIT
    dif_player = 0                                                                     # diferenca entre blackjack e o valor da mao do dealer
    if(player_hand_Ace):                                                               # Caso a mao do dealer contenha 1 ou mais Ace's
        if(player_value!=player_totalValue):
            dif_player = 21 - (player_totalValue - (player_hand_nAce * 10))            # teremos que subtratir o o numero de Ace * 10
    else:
        dif_player = 21 - player_value;

    num_benefit_cards_player = len([x for x in value_cards if dif_player >= x])      # numer de cartas beneficas para o player
    prob_player_not_bust = 1.0*num_benefit_cards_player/13                           # probabilidade de player melhorar a sua mao
    prob_player_bust = 1- (1.0*prob_player_not_bust)                                 # probabilidade de o player fazer bust


    return [prob_player_not_bust,prob_player_bust]

def dealer_probability(self,dealer):
    value_cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    dealer_value = card.value(dealer.hand) if card.value(dealer.hand) <= 21 else 0  # value cards dealer

    dealer_hand_Ace = False                                                         # mao do dealer contem Ace
    dealer_hand_nAce = 0                                                            # numero de Ace's visiveis do dealer
    if any(c.is_ace() for c in dealer.hand):
        dealer_hand_Ace =  True
    for c in dealer.hand:
        if c.is_ace():
            dealer_hand_nAce += 1;

    dealer_totalValue = 0                                                            # valor total da mao do player

    for c in dealer.hand:
        if c.is_ace():
            dealer_totalValue += c.value() + 10
        else:
            dealer_totalValue += c.value()

    dif_dealer = 0                                                                     # diferenca entre blackjack e o valor da mao do dealer
    if(dealer_hand_Ace):                                                               # Caso a mao do dealer contenha 1 ou mais Ace's
        if(dealer_value!=dealer_totalValue):
            dif_dealer = 21 - (dealer_totalValue - (dealer_hand_nAce * 10))            # teremos que subtratir o o numero de Ace * 10
    else:
        dif_dealer = 21 - dealer_value;

    num_benefit_cards_dealer = len([x for x in value_cards if dif_dealer >= x])      # numer de cartas beneficas para o dealer
    #print num_benefit_cards_dealer

    prob_dealer_not_bust = 1.0*num_benefit_cards_dealer/13                           # probabilidade de dealer melhorar a sua mao
    prob_dealer_bust = 1- (1.0*prob_dealer_not_bust)

    return [prob_dealer_not_bust,prob_dealer_bust]

def agressive_power(self):

    return 0

def writeVal_file(self,val):                                                         # guarda info de jogadas no ficheiro
    fileobj = open("values.txt","w")
    fileobj.write(str(val) + '\n')
    fileobj.close()

def readFile(self):                                                                 # lê info de jogadas no ficheiro
    fileobj = open("values.txt","r")
    info = fileobj.read()
    fileobj.close()
    return info