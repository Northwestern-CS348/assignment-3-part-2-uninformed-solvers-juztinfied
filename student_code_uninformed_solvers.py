
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
        moverecord = list()
        countrecord = [0]

        initial = self.gm.getGameState()

        solved = False 
        while not solved:
            moves = self.gm.getMovables() # this is a list of legal moves
            if not moves: # if there are no more available moves, need to backtrack
                self.gm.reverseMove(moverecord.pop())
                countrecord[-1] = countrecord[-1] + 1
                continue 
            else: # if there is at least one move to do
                self.gm.makeMove(moves[countrecord[-1]]) # do the first move offered 
                moverecord.append(moves[countrecord[-1]]) # record that move 
                next = self.gm.getGameState() # get the new state
                print(next)
                if next == self.victoryCondition: # check if victory is achieved 
                    solved = True 
                else: # if still no victory 
                    countrecord.append(0) # prepare this for next move 

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
        ### Student code goes here
        return True
