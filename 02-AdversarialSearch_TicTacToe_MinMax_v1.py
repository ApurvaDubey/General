print '''
This is a bot for tic-tac-toe using MinMax Search
There is no alpha-beta pruning done in this implementation

@author: Apurva Dubey

Player1: has to choose 'x'
Player2: has to choose 'o'

Below are positions in the board:
['1', '2', '3']
['4', '5', '6']
['7', '8', '9']
-------------------------------
'''
import copy

# set some constants
inf = 10**10 
player1 = 'x'
player2 = 'o'

class board():
    '''
    Class to set the Tic Tac Toe
    '''

    winConfigs = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],
                    [1,4,7],[2,5,8],[0,4,8],[2,4,6]]

    def __init__(self,in_posStates=[]):
        '''Initialize board'''
        if in_posStates == []:
            self.posStates = ["_" for i in range(0,9)]
        else:
            self.posStates = in_posStates

    def boardUpdate(self,move,curPlayer):
        '''Updae board with move of the player'''
        self.posStates[move] = curPlayer

    def availableMoves(self):
        '''find the set of available moves'''
        return [i for i,j in enumerate(self.posStates) if j in "_"]

    def show(self):
        '''print the state of the board'''
        print [self.posStates[i] for i in range(0,3)]
        print [self.posStates[i] for i in range(3,6)]
        print [self.posStates[i] for i in range(6,9)]
        print "--------------------------"

    def userInput(self,curPlayer):
        '''get input from the user'''
        inpt = None
        print "Turn for player:", curPlayer
        while 1==1:
            try:
               inpt = int(raw_input("Enter your move, value between [1,9]:"))-1
            except ValueError:
               pass
            
            if inpt not in self.availableMoves():
                print "***Please enter a legal move***"
            else:
                break
            
        self.boardUpdate(int(inpt),curPlayer)
        self.show()

    def getSuccessors(self,curPlayer):
        '''get successive board configurations based on available moves'''
        successors = {} # dictionary of move:result_state
        for m in self.availableMoves():
            tmp = copy.deepcopy(self.posStates)
            tmp[m] = curPlayer

            successors[m] = board(tmp)

        return successors

    def gameOver(self,verbose=False):
        '''check if the game is over or not, returning appropriate flags'''
        status = False # game is not over
        utility = 0

        player1Config = [i for i,v in enumerate(self.posStates) if v == 'x']
        player2Config = [i for i,v in enumerate(self.posStates) if v == 'o']

        for w in self.winConfigs: # loop thru winning configs
            cnt1 = 0
            cnt2 = 0
            for k in w:
                if k in player1Config:
                    cnt1 = cnt1 + 1
                if k in player2Config:
                    cnt2 = cnt2 + 1
            if cnt1 == 3:
                status = True # game over and 'x' won
                utility = 1
                if verbose == True:
                    print 'Game over and player1(\'x\') has won'
                break
            if cnt2 == 3:
                status = True # game over and 'o' won
                utility = -1
                if verbose == True:
                    print 'Game over and player2(\'o\') has won'
                break        

        if status == False and sum([1 for i in self.posStates if i == '_']) == 0:
            status = True # game over and tied
            utility = 0
            if verbose == True:
                print 'Game over and game has tied'

        return [status, utility]


def findBestMove(candidateMoves,flag):
    '''find the best move from the set of available (candidate) moves'''
    if flag == "min":
        bestUtility = +inf
        for move,utility in candidateMoves.items():
            if utility < bestUtility:
                bestUtility = utility
                bestMove = move

    if flag == "max":
        bestUtility = -inf
        for move,utility in candidateMoves.items():
            if utility > bestUtility:
                bestUtility = utility
                bestMove = move

    return [bestMove,bestUtility]


def minMove(gameNode):
    '''get move for the Minimizer player'''
    # if game is over then return terminal utility
    flag = gameNode.gameOver()
    if flag[0] == True:
        return [None,flag[1]]

    # else return a move that minimizes utility
    else:    
        candidateMoves = {}
        curPlayer = player2
        
        nextGameNodes = gameNode.getSuccessors(curPlayer)
        for move, nextGameNode in nextGameNodes.items():
            candidateMoves[move] = maxMove(nextGameNode)[1]

        return findBestMove(candidateMoves,'min')
    
def maxMove(gameNode):
    '''get move for the maximizer player'''
    # if game is over then return terminal utility
    flag = gameNode.gameOver()
    if flag[0] == True:
        return [None,flag[1]]

    # else return a move that maximizes utility
    else:  
        candidateMoves = {}
        curPlayer = player1
        
        nextGameNodes = gameNode.getSuccessors(curPlayer)
        for move, nextGameNode in nextGameNodes.items():
            candidateMoves[move] = minMove(nextGameNode)[1]

        return findBestMove(candidateMoves,'max')

def minMax(curPlayer,gameNode):
    '''main function for min-max'''
    if curPlayer == player2:
        return minMove(gameNode)[0]
    else:
        return maxMove(gameNode)[0]

def example():
    '''random example for unit testing'''
    b = board(['x', 'o', '_', 'x', 'o', 'o', '_', 'x', 'x'])
    b.show()
    print b.gameOver()
    print minMax(curPlayer,b)
    b.boardUpdate(minMax(curPlayer,b),curPlayer)
    b.show()

if __name__=="__main__":

    # set the board
    b = board()
    b.show()

    # player1 and player2 make moves alternately
    while b.gameOver()[0] == False:

        # check whose chance it is
        if b.posStates.count('x') - b.posStates.count('o') == 0:
            curPlayer = player1
        else:
            curPlayer = player2

        # take input from current player
        if curPlayer == player1:
            b.userInput(curPlayer)
            b.gameOver(verbose=True)
        else:
            b.boardUpdate(minMax(curPlayer,b),curPlayer)
            b.show()
            b.gameOver(verbose=True)
    


