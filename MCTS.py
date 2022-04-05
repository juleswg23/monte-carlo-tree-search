#from copy import deepcopy
import random
from Connect4 import Connect4
from sys import maxsize
from math import sqrt, log
from time import time
from timeit import timeit

class NodeState():    
    def __init__ (self, state):
        self.state = state
        self.visitCount = 0.0
        self.winCount = 0.0
    
    def __str__(self):
        toPrint = "NodeState:\n"
        toPrint += "Visit Count: " + str(self.visitCount) + " Win Count: " + str(self.winCount) + "\n"
        toPrint += str(self.state) + "\n"
        return toPrint
    
    def getState(self):## -> MegaBoard
        return self.state
    
    def setState(self, state):##(_ megaBoard: MegaBoard) -> Void  
        self.state = state
    
    def getVisitCount(self):## -> Int  
        return self.visitCount
    
    def incrementVisitCount(self):## -> Void  
        self.visitCount += 1.0
    
    def getWinCount(self):## -> Double  
        return self.winCount
    
    def addToWinCount(self, toAdd):##(_ count: Double) -> Void  
        self.winCount += toAdd
    
    def getAllPossibleStates(self):## -> [State]
        result = []
        for move in self.getState().get_possible_moves():
            newState = self.getState().deepcopy()
            newState.make_move(move)
            result.append(newState)
        return result
    
    def randomPlay(self):## -> Void
        self.getState().random_move()
        #self.getState().smart_random_move()

class MCTSNode():    
    def __init__(self, nodeState):
        self.nodeState = nodeState
        self.parent = None
        self.children = []
    
    def __str__(self):
        toPrint = "MCTSNode:\n"
        toPrint += str(self.nodeState) + "\n"
        toPrint += "Parent: " + ("yes" if self.parent != None else "no") + "\n"
        toPrint += "Num children: " + str(len(self.children)) + "\n"
        return toPrint
    
    def getNodeState(self):## -> GamenodeState
        return self.nodeState
    
    def getParent(self):## -> MCTSNode?  
        return self.parent
    
    def setParent(self, parent):##_ parent: MCTSNode) -> Void  
        self.parent = parent
    
    def getChildren(self):## -> [MCTSNode]  
        return self.children
    
    def addToChildren(self, child):## -> Void  
        self.children.append(child)
    
    def getRandomChild(self): ## -> MCTSNode  
        return random.choice(self.children)

class MCTS():
    def __init__(self, depthTime):
        self.depthTime = depthTime
        self.aiPlayer = None
        self.opponent = None
        self.root = None
    
    def findNextMove(self, state):##: MegaBoard) -> Void  
        self.aiPlayer = state.turn
        self.opponent = -state.turn
        self.root = MCTSNode(NodeState(state.deepcopy())) ## TODO: maybe no copy needed

        endTime = time() + self.depthTime
        while (time() < endTime):
            promisingNode = self.__selectPromisingNode(self.root)

            if promisingNode.getNodeState().getState().result == None:
                self.__expandNode(promisingNode)
            
            if len(promisingNode.getChildren()) > 0:
                promisingNode = promisingNode.getRandomChild()

            playoutResult = self.__simulateRandomPlayout(promisingNode)

            self.__backPropogation(promisingNode, playoutResult)
        
        max = -maxsize
        bestNode = None ##may ignore game over situations
        index = 0
        RUNS = 0
        WIN_COUNT = 0

        for node in self.root.getChildren():

            nodeScore = node.getNodeState().getWinCount() / node.getNodeState().getVisitCount()
            print("Move index: " + str(index) + " Score: " + str(node.getNodeState().getWinCount()) + "/" + 
                    str(node.getNodeState().getVisitCount()) + " = " + f'{nodeScore: .3f}')
            index += 1

            if node.getNodeState().getWinCount() >= 0: 
                WIN_COUNT += node.getNodeState().getWinCount()
            RUNS += node.getNodeState().getVisitCount()

            if nodeScore > max:
                max = nodeScore
                bestNode = node
        
        print("Win probability: " + f'{max:.3f}')
        print("Wins: " + str(WIN_COUNT) + " out of "+ str(RUNS) + " runs.")

        return bestNode.getNodeState().getState()
    
    def __selectPromisingNode(self, rootNode):## -> MCTSNode  
        node = rootNode
        while (len(node.getChildren())!= 0):
            node = UCT.findBestNodeWithUCT(node)
        return node

    
    def __expandNode(self, node):##_ node: MCTSNode) -> Void  
        for state in node.getNodeState().getAllPossibleStates():
            newNode = MCTSNode(NodeState(state))
            newNode.setParent(node)
            node.addToChildren(newNode)

    
    def __simulateRandomPlayout(self, node):
        tempNodeState = NodeState(node.getNodeState().getState().deepcopy())
        boardStatus = tempNodeState.getState().result
        if boardStatus == self.opponent:
            node.getParent().getNodeState().addToWinCount(-maxsize)
            return boardStatus
        while (boardStatus == None):
            tempNodeState.randomPlay()
            boardStatus = tempNodeState.getState().result
        return boardStatus
    
    def __backPropogation(self, node, result):## MCTSNode, result: Status) -> Void  
        tempNode = node
        while (tempNode != None):
            # print(tempNode.getNodeState().getState().turn)
            tempNode.getNodeState().incrementVisitCount()
            if tempNode.getNodeState().getState().turn == -result:
                tempNode.getNodeState().addToWinCount(1.0)
            elif result == 0:
                tempNode.getNodeState().addToWinCount(0.5)
            tempNode = tempNode.getParent()


class UCT():
    @staticmethod
    def uctValue(totalVisit, nodeWinCount, nodeVisitCount):
        if nodeVisitCount == 0:
            return maxsize
        
        a = nodeWinCount / nodeVisitCount
        b =  sqrt( log(totalVisit) / nodeVisitCount )
        return a + (1.4142857*b)
 
    @staticmethod
    def findBestNodeWithUCT(node): ## -> MCTSNode {
        parentVisit = node.getNodeState().getVisitCount()
        best = node.getChildren()[0]
        max = -maxsize
        
        for child in node.getChildren():
            newUCT = UCT.uctValue(parentVisit, child.getNodeState().getWinCount(), child.getNodeState().getVisitCount())
            if newUCT > max:
                max = newUCT
                best = child
        return best

if __name__ == "__main__":
    board = Connect4()
    thinkTime = None
    userFirst = None

    while thinkTime == None:
        print("How much time should the computer think for?")
        try:
             answer = int(input())
        except:
            continue
        if answer != 0:
            thinkTime = answer

    while userFirst == None:
        print("Would you like to go first? (Y/N)")
        answer = input()
        if answer == "N" or answer == "n":
            ai = MCTS(depthTime = thinkTime)
            print("Running...")
            board = ai.findNextMove(state = board)
            print(board)
            userFirst = "N"
        elif answer == "Y" or answer == "y":
            print(board)
            print("Your Turn")
            userFirst = "Y"


    while board.result == None:
        move = int(input())-1
        board.make_move(move)
        if board.result != None:
            print("You Win!")
            break

        ai = MCTS(depthTime = thinkTime)
        print("Running...")
        print(board)
        board = ai.findNextMove(state = board)
        
        print(board)
        if board.result != None:
            print("Computer Wins!")
            break
        print("Your Turn")
    print("Game Over")