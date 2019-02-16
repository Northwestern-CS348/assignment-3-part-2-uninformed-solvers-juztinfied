from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        
        # we first need to ask the KB of the parent class 

        # enquire for peg1
        ask1 = parse_input("fact: (on ?X peg1)")
        answers = self.kb.kb_ask(ask1)
        p1 = list()

        if not answers:
            pass 
        else:
            for answer in answers:
                if (not answer):
                    continue
                reply = str(answer)
                p1.append(int(reply[-1]))

        # enquire for peg2
        ask1 = parse_input("fact: (on ?X peg2)")
        answers = self.kb.kb_ask(ask1)
        p2 = list()

        if not answers:
            pass
        
        else: 
            for answer in answers:
                reply = str(answer)
                p2.append(int(reply[-1]))

        # enquire for peg3
        ask1 = parse_input("fact: (on ?X peg3)")
        answers = self.kb.kb_ask(ask1)
        p3 = list()
        if not answers:
            pass

        else: 
            for answer in answers:
                reply = str(answer)
                p3.append(int(reply[-1]))

        # create the tuples from the lists
        p1.sort()
        p2.sort()
        p3.sort()
        peg1 = tuple(p1)
        peg2 = tuple(p2)
        peg3 = tuple(p3)

        return (peg1, peg2, peg3)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        terms = movable_statement.terms
        disktomove = terms[0].__str__()
        oldpeg = terms[1].__str__()
        newpeg = terms[2].__str__()

        # find out what disk is below target disk 
        print ('asking what is the disk below target disk')
        ask = parse_input("fact: (ontop %s ?X)" %disktomove)
        answer = self.kb.kb_ask(ask)

        if not answer:
            print ('no answer')
        
        diskbelow = str(answer[0])
        diskbelow = diskbelow[-5:]
        print (diskbelow)

        # find out what is currently at the top of new peg
        print ('asking what is currently at the top of new peg')
        ask = parse_input("fact: (ontop ?X %s)" %newpeg)
        answer = self.kb.kb_ask(ask)
        topofnewpegdisk = ''
        if not answer:
            topofnewpegdisk = 'base1'
            print (topofnewpegdisk)
        else:
            topofnewpegdisk = str(answer[0])
            topofnewpegdisk = topofnewpegdisk[-5:]
            print ('top of new peg disk is:')
            print (topofnewpegdisk)

        # first we need to retract fact that the disk is at old peg
        statement1 = Statement(['on', disktomove, oldpeg])
        fact1 = Fact(statement1)
        # second, we need to assert fact that disk is on new peg
        statement2 = Statement(['on', disktomove, newpeg])
        fact2 = Fact(statement2)
        # next, assert that the disk below target disk is at the top of old peg
        statement3 = Statement(['top', diskbelow])
        fact3 = Fact(statement3)
        # also assert what the target disk is on top of
        statement4 = Statement(['ontop', disktomove, topofnewpegdisk])
        fact4 = Fact(statement4)
        # need to retract the fact that the new peg as a new top most disk
        fact5 = 0
        if topofnewpegdisk == 'base1':
            pass
            print ('no need for fact 5')
        else:
            print ('we need fact 5')
            statement5 = Statement(['top', topofnewpegdisk])
            fact5 = Fact(statement5)
            print (fact5)

        self.kb.kb_retract(fact1)
        self.kb.kb_assert(fact2)
        self.kb.kb_assert(fact3)
        self.kb.kb_assert(fact4)
        if fact5:
            self.kb.kb_retract(fact5)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
