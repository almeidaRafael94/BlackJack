from game import Game
from player import Player
from randomplayer import RandomPlayer
from student import StudentPlayer

if __name__ == '__main__':

    players = [StudentPlayer("Paulo",1000),StudentPlayer("Martins",1000),StudentPlayer("Marco",1000),StudentPlayer("Xico",1000), RandomPlayer("random",1000)]

    for i in range(5000):
        print players
        print "\nIteracao: " + str(i) + "\n"
        g = Game(players, min_bet=1, max_bet=100) 
        #g = Game(players, debug=True)
        g.run()

    print "OVERALL: ", players
