
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        statemovesrecord = dict()
        moverecords = list()
        initial = self.gm.getGameState()
        statemovesrecord[initial] = -1
        solved = False

        while True:
            print('look at the state move records: ' + statemovesrecord)
            # know what is the current node its on
            current = self.gm.getGameState()
            print('current state:' + current)
            # check for victory condition
            if current == self.victoryCondition:
                solved = True
                break 

            # get all possible child nodes 
            moves = self.gm.getMovables()
            print(moves)
            if moves:  # if there are child nodes 
                # if we have not visited this current node before
                if current not in statemovesrecord:
                    statemovesrecord[current] = 0 # we are going to try the first available child first
                    for move in moves: # for each child
                        if statemovesrecord[current] != moves.index(move):
                            print('error')

                        self.gm.makeMove(moves[statemovesrecord[current]]) # visit leftmost child node 
                        next = self.gm.getGameState()
                        print('trying move')
                        print(moves[statemovesrecord[current]])
                        moverecords.append(moves[statemovesrecord[current]]) # record move

                        # if this child is a state we visited before, do not expand this child. try another child
                        if next in statemovesrecord: 
                            print('visited before!')
                            self.gm.reverseMove(moverecords.pop()) # go back to current
                            statemovesrecord[current] += 1
                            if statemovesrecord[current] >= len(moves): # if we ran out of child nodes to go to
                                # reverse last move. go back to parent node 
                                self.gm.reverseMove(moverecords.pop())
                                continue # repeat loop 
                            else:
                                self.gm.makeMove(moves[statemovesrecord[current]]) # visit an unvisited child node
                                moverecords.append(moves[statemovesrecord[current]]) # record move 
                                continue 
                                #print('chosen move')
                                #print(moves[statemovesrecord[current]])
                        else: # if we have not visited this child before, set this child as next current node
                            self.gm.makeMove(moves[statemovesrecord[current]]) # visit an unvisited child node
                            moverecords.append(moves[statemovesrecord[current]]) # record move 
                            continue 

                    continue # repeat loop to expand next state

                # if we ever reach this current node before, go to a child not visited before
                else:
                    statemovesrecord[current] += 1
                    if statemovesrecord[current] >= len(moves): # if we ran out of child nodes to go to
                        # reverse last move. go back to parent node 
                        self.gm.reverseMove(moverecords.pop())
                        continue # repeat loop 
                    else:
                        self.gm.makeMove(moves[statemovesrecord[current]]) # visit an unvisited child node
                        moverecords.append(moves[statemovesrecord[current]]) # record move 
                        #print('chosen move')
                        #print(moves[statemovesrecord[current]])
            
            else: # if there are no child nodes 
                # reverse last move. go back to parent node 
                self.gm.reverseMove(moverecords.pop())

            if solved or not moverecords:
                break 

        return solved 
            
            
            
class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        pathtostate = dict()
        initial = self.gm.getGameState
        pathtostate[initial] = []
        solved = False

        while True:
            # know what is the current node its on
            current = self.gm.getGameState()
            # get path to current state
            pathtocurrent = pathtostate[current]
            # check for victory condition
            if current == self.victoryCondition:
                solved = True
                break 

            # get all possible child nodes 
            moves = self.gm.getMovables()
            if moves:  # if there are child nodes 
                for move in moves: # for each child
                    self.gm.makeMove(move)
                    childstate = self.gm.getGameState 
                    if childstate == self.victoryCondition: # if child is solution
                        solved = True
                        break # end while loop 
                    else: # if child is not solution
                        pathtochild = pathtocurrent.append(move) # path to child is path to current + move
                        pathtostate[childstate] = pathtochild # record path to child
                        self.gm.reverseMove(move) # go back to the parent and explore another child 

            else: # if current is a leaf node and is also not the solution
                # go back to root
                pathtoroot = pathtostate[current]
                pathtostate.remove(current)
                for i in range(len(pathtoroot)):
                    self.gm.reverseMove(pathtoroot.pop())

            if pathtostate: # if there is still at least one node to expand
                # go to that node 
                pathtonewcurrent = pathtostate.pop(0)
                for i in range(len(pathtonewcurrent)):
                    self.gm.makeMove(pathtonewcurrent[i])

                continue 

            else: # if there are no more nodes to explore 
                break 


        return solved