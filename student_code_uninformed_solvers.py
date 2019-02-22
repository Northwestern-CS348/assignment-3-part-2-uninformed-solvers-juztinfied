
from solver import *

class SolverDFS(UninformedSolver):
    statemovesrecord = dict()
    moverecords = list()
    
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
        current = self.gm.getGameState()
        # print('current state:')
        # print(current)
        # print('look at the state records: ')
        # print(self.statemovesrecord)

        # check for victory condition
        if current == self.victoryCondition:
            # print ('solved!')
            return True 

        # get all possible child nodes 
        moves = self.gm.getMovables()
        if moves:  # if there are child nodes 
            # if we have not visited this current node before
            if current not in self.statemovesrecord:
                for move in moves: # for each child
                    self.statemovesrecord[current] = moves.index(move)
                    self.gm.makeMove(move) # visit leftmost child node 
                    next = self.gm.getGameState()
                    # print('trying move')
                    # print(move)
                    self.moverecords.append(move) # record move

                    # if this child is a state we visited before, do not expand this child. try another child
                    if next in self.statemovesrecord: 
                        self.gm.reverseMove(self.moverecords.pop()) # go back to current
                        # reverse last move. go back to parent node 
                        continue # repeat loop to try another child

                    else: # if we have not visited this child before, set this child as next current node
                        return False 

                # if we get to this part of the code, it means we ran out of child nodes
                if self.statemovesrecord[current] >= len(moves):
                    self.gm.reverseMove(self.moverecords.pop())
                    return False 

            # if we ever reach this current node before, go to a child not visited before
            else:
                self.statemovesrecord[current] += 1
                if self.statemovesrecord[current] >= len(moves): # if we ran out of child nodes to go to
                    # reverse last move. go back to parent node 
                    self.gm.reverseMove(self.moverecords.pop())
                    return False 
                else:
                    self.gm.makeMove(moves[self.statemovesrecord[current]]) # visit an unvisited child node
                    self.moverecords.append(moves[self.statemovesrecord[current]]) # record move 
                    return False 
            
        else: # if there are no child nodes 
            # reverse last move. go back to parent node 
            self.gm.reverseMove(self.moverecords.pop())
            return False 
            
            
class SolverBFS(UninformedSolver):
    pathtostate = dict()
    initial = 0
    junk = list() 
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        initial = gameMaster.getGameState()
        self.pathtostate[initial] = []

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
        # know what is the current node its on
        current = self.gm.getGameState()
        print('current')
        print(current)
        print('state queue')
        print(list(self.pathtostate.keys()))
        # get path to current state
        pathtocurrent = self.pathtostate[current]

        if current == self.victoryCondition:
            return True 
        # remove itself from state queue
        self.junk.append(current)
        self.pathtostate.pop(current)
        # check for victory condition


        # get all possible child nodes 
        moves = self.gm.getMovables()
        if moves:  # if there are child nodes 
            for move in moves: # for each child
                print('start of move loop')
                self.gm.makeMove(move) # move to that child
                childstate = self.gm.getGameState() # get that child's state 
                print('new state')
                print(childstate)
                if childstate in self.junk: # if child node has been visited before
                    print('been there')
                    self.gm.reverseMove(move)
                    continue
                pathtochild = pathtocurrent + [move] # path to child is path to current + move
                self.pathtostate[childstate] = pathtochild # record path to child in state queue 
                self.gm.reverseMove(move)
                # if childstate == self.victoryCondition: # if child is solution
                #     return True 
                #else: # if not a solution, go back to parent and repeat loop to explore another child 
                    #self.gm.reverseMove(move) 

            # if none of the children are victory condition
            while pathtocurrent:
                self.gm.reverseMove(pathtocurrent.pop()) # go back to root

            if len(self.pathtostate):
                nextstate = list(self.pathtostate.keys())[0]
                pathtonext = self.pathtostate[nextstate] # find the path to the first node in the state queue 
                for step in pathtonext:
                    self.gm.makeMove(step)
                return False
            
            else:
                return False 

        else: # if current is a leaf node and is also not the solution
            # go back to root
            while pathtocurrent:
                self.gm.reverseMove(pathtocurrent.pop())

            if len(self.pathtostate):
                pathtonext = self.pathtostate[self.pathtostate.keys()[0]]
                for step in pathtonext:
                    self.gm.makeMove(step)
                return False 

            else: # if there are no more nodes to explore 
                return False 

        # while True:
        #     # know what is the current node its on
        #     current = self.gm.getGameState()
        #     # get path to current state
        #     pathtocurrent = pathtostate[current]
        #     # check for victory condition
        #     if current == self.victoryCondition:
        #         solved = True
        #         break 

        #     # get all possible child nodes 
        #     moves = self.gm.getMovables()
        #     if moves:  # if there are child nodes 
        #         for move in moves: # for each child
        #             self.gm.makeMove(move)
        #             childstate = self.gm.getGameState 
        #             if childstate == self.victoryCondition: # if child is solution
        #                 solved = True
        #                 break # end while loop 
        #             else: # if child is not solution
        #                 pathtochild = pathtocurrent.append(move) # path to child is path to current + move
        #                 pathtostate[childstate] = pathtochild # record path to child
        #                 self.gm.reverseMove(move) # go back to the parent and explore another child 

        #     else: # if current is a leaf node and is also not the solution
        #         # go back to root
        #         pathtoroot = pathtostate[current]
        #         pathtostate.remove(current)
        #         for i in range(len(pathtoroot)):
        #             self.gm.reverseMove(pathtoroot.pop())

        #     if pathtostate: # if there is still at least one node to expand
        #         # go to that node 
        #         pathtonewcurrent = pathtostate.pop(0)
        #         for i in range(len(pathtonewcurrent)):
        #             self.gm.makeMove(pathtonewcurrent[i])

        #         continue 

        #     else: # if there are no more nodes to explore 
        #         break 


        # return solved