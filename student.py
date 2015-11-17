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
from collections import Counter


class StudentPlayer(Player):
    def __init__(self, name="Student", money=0):
        super(StudentPlayer, self).__init__(name, money)

    def play(self, dealer, players):

        player = [x for x in players if x.player.name == self.name][0]  # player = my boot (name = Student)
        dealer_value = card.value(dealer.hand) if card.value(dealer.hand) <= 21 else 0  # value cards dealer
        player_value = card.value(player.hand) if card.value(player.hand) <= 21 else 0  # value cards my boot

        #print "Dealer_Hand: [%s]" % str(dealer.hand)
        #print "Dealer_value: %d" % dealer_value
        #print "Player_Hand: [%s]" % player.hand
        #print "Player_value: %d" % player_value

        player_probs = player_probability(self, player)
        player_prob_bust = player_probs[0]
        player_prob_not_bust = 1 - player_prob_bust
        player_prob_better_hand = player_probs[1]

        dealer_probs = dealer_probability(self, dealer)
        dealer_prob_bust = dealer_probs[0]
        dealer_prob_not_bust = 1 - dealer_prob_bust
        dealer_prob_better_hand = dealer_probs[1]
        dealer_prob_hit = dealer_probs[2]

        #print "++++++++++++PLAYER[Bust , Better_hand]+++++++++++++++++"
        #print player_probs
        #print "++++++++++++DEALER[Bust , Better_hand, Prob_hit]+++++++++++++++++"
        #print dealer_probs
        #print "++++++++++++++++++++++++++++++++++++++++++++++++++++"

        '''
        strtmp = readFile(self)
        strtmp += "\nPlayer_value " + str(player_value)
        strtmp += "\nPlayer_Bust "  + str(player_prob_bust)
        strtmp += "\nPlayer_NOT_BUST " + str(player_prob_not_bust)
        strtmp += "\nPlayer_better_hand " + str(player_prob_better_hand)
        strtmp += "\nDealer_value " + str(dealer_value)
        strtmp += "\nDealer_Bust "  + str(dealer_prob_bust)
        strtmp += "\nDealer_NOT_BUST " + str(dealer_prob_not_bust)
        strtmp += "\nDealer_better_hand " + str(dealer_prob_better_hand)
        strtmp += "\nDealer_prob_hit " + str(dealer_prob_hit)
        '''
        fileobj = open("last_dealer_value.txt", "r")
        last_dealer_value = fileobj.read()
        fileobj.close()

        fileobj = open("last_dealer_value.txt", "w")
        fileobj.write(str(dealer_value) + '\n')
        fileobj.close()


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

        op = ""

        if(int(dealer_value) == int(last_dealer_value)):                              # dealer fez stand
            #strtmp += "\nCondition: Dealer fez stand, já tem 17 pontos"
            if(player_value <= 17):
                op = "h"
            else:
                op = "s"

        elif(dealer_value > 17):
            op = "s"
            #strtmp += "\nCondition: dealer_value > 17"
        elif(player_prob_better_hand >= 0.65):
            op = "h"
            #strtmp += "\nCondition: prob_Player_BH >= 0.65"
        elif(player_value>16):
            op = "s"
            #strtmp += "\nCondition: Player_value > 16"
        elif(dealer_prob_bust >= 0.80):
            op = "s"
            #strtmp += "\nCondition: Dealer_prob_BUST >= 0.8"
        elif(player_value == 16):
            #strtmp += "\nCondition: Player_value = 16"
            if(dealer_value > 14 and dealer_prob_bust <= 0.5):
                op = "h"
            else:
                op = "s"
        elif(dealer_prob_bust > 0.7 and dealer_prob_bust < 0.8):
            #strtmp += "\nCondition: Dealer_prob_bust ]0.7 , 0.8[ "
            if(player_prob_bust >= 0.7):
                cmd = ["h", "s"]
                op = cmd[random.randint(0,1)]
            elif(player_prob_bust <= 0.3):
                op = "h"
            else:
                cmd = ["h","h", "h", "s"]
                op = cmd[random.randint(0,3)]

        elif(dealer_prob_bust > 0.5 and dealer_prob_bust <= 0.7):
            #strtmp += "\nCondition: Dealer_prob_bust ]0.5 , 0.7] "
            if(player_prob_better_hand >= 0.6):
                op = "h"
            elif(dealer_prob_better_hand >= 0.6):
                op = "h"
            else:
                op = "s"
        else:
            #strtmp += "\nCondition: Dealer_prob_bust <= 0.4 "
            if(player_prob_better_hand <= 0.40):
                op = "s"
            else:
                op = "h"

        #strtmp += "\nOP -> " + op
        #writeVal_file(self,strtmp)
        return op

    def bet(self, dealer, players):
        cmd = [1]
        return cmd[random.randint(0, 0)]


def player_probability(self, player):  # return [prob_not_bust,prob_bust]
    value_cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  # cards value
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
    dif_player = 0                                                  # diferenca entre blackjack e o valor da mao do dealer
    if (player_hand_Ace):                                           # Caso a mao do dealer contenha 1 ou mais Ace's
        if (player_value != player_totalValue):
            dif_player = 21 - (
            player_totalValue - (player_hand_nAce * 10))            # teremos que subtratir o o numero de Ace * 10
    else:
        dif_player = 21 - player_value;

    num_benefit_cards_player = len(
        [x for x in value_cards if dif_player >= x])  # numer de cartas beneficas para o player
    prob_player_not_bust = 1.0 * num_benefit_cards_player / 13  # probabilidade de player melhorar a sua mao
    prob_player_bust = 1 - (1.0 * prob_player_not_bust)  # probabilidade de o player fazer bust

    if (player_hand_Ace):  # calcular probabilidade de melhorar mao em caso de "h"
        prob_better_hand = 1.0 * (21 - player_value) / 13
    else:
        prob_better_hand = prob_player_not_bust

    return [prob_player_bust, prob_better_hand]


def dealer_probability(self, dealer):
    value_cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    dealer_value = card.value(dealer.hand) if card.value(dealer.hand) <= 21 else 0  # value cards dealer

    dealer_hand_Ace = False  # mao do dealer contem Ace
    dealer_hand_nAce = 0  # numero de Ace's visiveis do dealer
    if any(c.is_ace() for c in dealer.hand):
        dealer_hand_Ace = True
    for c in dealer.hand:
        if c.is_ace():
            dealer_hand_nAce += 1;

    #print "\ndealer_hand_Ace : %s" % str(dealer_hand_Ace)
    #print "\ndealer_hand_nAce: %s" % str(dealer_hand_nAce)

    dealer_totalValue = 0  # valor total da mao do player

    for c in dealer.hand:
        if c.is_ace():
            dealer_totalValue += c.value() + 10
        else:
            dealer_totalValue += c.value()

    #print "\ndealer_totalValue: %d" % dealer_totalValue

    dif_dealer = 0                                          # diferenca entre blackjack e o valor da mao do dealer
    if (dealer_hand_Ace):
        #print "\nMao do delaer contem ACE"                                                        # Caso a mao do dealer contenha 1 ou mais Ace's
        if (dealer_value != dealer_totalValue):
            dif_dealer = 21 - (
            dealer_totalValue - (dealer_hand_nAce * 10))    # teremos que subtratir o o numero de Ace * 10
    else:
        dif_dealer = 21 - dealer_value;

    #print "\ndif_dealer: %d" % dif_dealer

    num_benefit_cards_dealer = len(
        [x for x in value_cards if dif_dealer >= x])        # numer de cartas beneficas para o dealer
    #print num_benefit_cards_dealer

    #print "\nnum_benefit_cards_dealer: %d" % num_benefit_cards_dealer

    prob_dealer_not_bust = 1.0 * num_benefit_cards_dealer / 13  # probabilidade de dealer melhorar a sua mao
    prob_dealer_bust = 1 - (1.0 * prob_dealer_not_bust)

    if (dealer_hand_Ace):  # calcular probabilidade de melhorar mao
        prob_better_hand = 1.0 * (21 - dealer_value) / 13
    else:
        prob_better_hand = prob_dealer_not_bust

    count = 0
    for c in value_cards:
        if (c <= (17 - dealer_value)):
            count += 1

    if (dealer_value < 17):                                             # probabilidade do dealer fazer hit na proxima jogada
        if (dealer_value <= 10):
            if(count > 12):
                count = 12;
            prob_hit = 1.0 * (count + 1) / 13                           # +1 porque o Ace é favorável neste caso
        else:
            prob_hit = 1.0 * (count) / 13
    else:
        prob_hit = 0

    return [prob_dealer_bust, prob_better_hand, prob_hit]


def agressive_power(self):
    return 0


def save_dealer_move(self, dealer_hand):
    return 0


def writeVal_file(self, val):  # guarda info de jogadas no ficheiro
    fileobj = open("values.txt", "w")
    fileobj.write(str(val) + '\n')
    fileobj.close()


def readFile(self):  # lê info de jogadas no ficheiro
    fileobj = open("values.txt", "r")
    info = fileobj.read()
    fileobj.close()
    return info
