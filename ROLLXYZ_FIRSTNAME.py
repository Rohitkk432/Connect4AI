#!/usr/bin/env python3
from FourConnect import * # See the FourConnect.py file
import csv
import gc

class GameTreePlayer:
    
    def __init__(self):
        pass

    def checkWinner(self,game):
        if game.winner == 1 :
            return 1
        elif game.winner == 2 :
            return 2
        else:
            return 0
        
    def CheckP1Col(self,state1,state2):
        for i in range(6):
            for j in range(7):
                if state1[i][j]!=state2[i][j]:
                    return j

    def MoveFinder(self,currentState,depth):
        if depth==0:
            return -1,0
        
        bestMove = -1
        rewards=[]
        winIndex=[]
        lossIndex=[]
        dkIndex=[]
    
        winNow = []
        p1WinCols=[]

        for action in range(7):
            fourConnectDummy = FourConnect()
            fourConnectDummy.SetCurrentState(currentState)
            gameWinner=0

            if currentState[0][action]==0:
                fourConnectDummy.GameTreePlayerAction(action)
                gameWinner = self.checkWinner(fourConnectDummy)
                
                if gameWinner!=2:
                    try:
                        state1 = fourConnectDummy.GetCurrentState()
                        fourConnectDummy.MyopicPlayerAction()
                        gameWinner = self.checkWinner(fourConnectDummy)

                        if gameWinner!=1:
                            stateNow = fourConnectDummy.GetCurrentState()
                            bestMove1,rewardBest1 = self.MoveFinder(stateNow,depth-1)
                            rewards.append(rewardBest1)
                        else:
                            state2 = fourConnectDummy.GetCurrentState()
                            p1Move = self.CheckP1Col(state1,state2)
                            p1WinCols.append(p1Move)
                            rewards.append(-1)
                    except AssertionError as e:  
                        rewards.append(0)
                else:
                    winNow.append(action)
                    rewards.append(1)
            else:
                rewards.append(-2)

            del fourConnectDummy
            gc.collect()

        for idx in range(7):
            if rewards[idx]==1:
                winIndex.append(idx)
            elif rewards[idx]==-1:
                lossIndex.append(idx)
            elif rewards[idx]==0:
                dkIndex.append(idx)
        
        if len(winNow)>0:
            rewardBest=1
            bestMove=random.choice(winNow)
        elif len(p1WinCols)>0:
            bestMove=random.choice(p1WinCols)
            rewardBest=rewards[bestMove]
        elif len(winIndex)>0:
            rewardBest=1
            bestMove=random.choice(winIndex)
        elif len(dkIndex)>0:
            rewardBest=0
            bestMove=random.choice(dkIndex)
        elif len(lossIndex)>0:
            rewardBest=-1
            bestMove=random.choice(lossIndex)
        else:
            rewardBest=-2
            bestMove=0

        # rewardBest = max(rewards,default=0)
        # bestMove = rewards.index(rewardBest)

        return bestMove,rewardBest
    
    def FindBestAction(self,currentState):
        """
        Modify this function to search the GameTree instead of getting input from the keyboard.
        The currentState of the game is passed to the function.
        currentState[0][0] refers to the top-left corner position.
        currentState[5][6] refers to the bottom-right corner position.
        Action refers to the column in which you decide to put your coin. The actions (and columns) are numbered from left to right.
        Action 0 is refers to the left-most column and action 6 refers to the right-most column.
        """
        
        bestMove,rewardBest = self.MoveFinder(currentState,5)
        
        # bestAction = input("Take action (0-6) : ")
        bestAction = bestMove
        return bestAction


def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open('testcase.csv', 'r') as read_obj: 
       	csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
        return testcaseState


def PlayGame():
    fourConnect = FourConnect()
    fourConnect.PrintGameState()
    gameTree = GameTreePlayer()
    
    move=0
    while move<42: #At most 42 moves are possible
        if move%2 == 0: #Myopic player always moves first
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    """
    You can add your code here to count the number of wins average number of moves etc.
    You can modify the PlayGame() function to play multiple games if required.
    """
    if fourConnect.winner==None:
        print("Game is drawn.")
    else:
        print("Winner : Player {0}\n".format(fourConnect.winner))
    print("Moves : {0}".format(move))
    return fourConnect.winner,move

def RunTestCase():
    """
    This procedure reads the state in testcase.csv file and start the game.
    Player 2 moves first. Player 2 must win in 5 moves to pass the testcase; Otherwise, the program fails to pass the testcase.
    """
    
    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseStateFromCSVfile()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move=0
    while move<5: #Player 2 must win in 5 moves
        if move%2 == 1: 
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    print("Roll no : 2021H10309999") #Put your roll number here
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
    print("Moves : {0}".format(move))
    

def main():
    
    # wins = 0
    # loss = 0
    # draw = 0
    # totalMovesInWin = 0
    # totalMovesInLoss = 0
    # totalMovesInDraw = 0

    # for times in range(50):
    #     gameWinner,move = PlayGame()
    #     if gameWinner==2:
    #         wins+=1
    #         totalMovesInWin+=move
    #     elif gameWinner==1:
    #         loss+=1
    #         totalMovesInLoss+=move
    #     else:
    #         draw+=1
    #         totalMovesInDraw+=move

    # print('-----50 Games-----\n')

    # if wins>0:
    #     avgMoveWin = totalMovesInWin/wins
    #     print('Wins: ',wins,', Avg Moves: ',avgMoveWin,'\n')

    # if loss>0:
    #     avgMoveLoss = totalMovesInLoss/loss
    #     print('Losses: ',loss,', Avg Moves: ',avgMoveLoss,'\n')

    # if draw>0 : 
    #     avgMoveDraw = totalMovesInDraw/draw
    #     print('Draws: ',draw,', Avg Moves: ',avgMoveDraw,'\n')


    # PlayGame()
    """
    You can modify PlayGame function for writing the report
    Modify the FindBestAction in GameTreePlayer class to implement Game tree search.
    You can add functions to GameTreePlayer class as required.
    """

    """
        The above code (PlayGame()) must be COMMENTED while submitting this program.
        The below code (RunTestCase()) must be UNCOMMENTED while submitting this program.
        Output should be your rollnumber and the bestAction.
        See the code for RunTestCase() to understand what is expected.
    """
    
    RunTestCase()


if __name__=='__main__':
    main()
