from game import Game
from player import Player
from randomplayer import RandomPlayer
from student import StudentPlayer

if __name__ == '__main__':

    players = [StudentPlayer("BOT_1",100),StudentPlayer("BOT_2",100),StudentPlayer("BOT_3",100),StudentPlayer("BOT_4",100)]
    for i in range(10000):

        print players
        
        print "\nIteracao: " + str(i) + "\n"
        '''
        fileobj = open("values.txt", "r")
        info = fileobj.read()
        fileobj.close()
        info += ("\nIteracao: %d"% i)
        fileobj = open("values.txt", "w")
        fileobj.write(str(info) + '\n')
        fileobj.close()
        '''

        g = Game(players, min_bet= 2, max_bet=100)
        #g = Game(players, debug=True)
        g.run()

    print "OVERALL: ", players
