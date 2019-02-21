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
        ask = parse_input("fact: (ontop %s ?X)" %disktomove)
        answer = self.kb.kb_ask(ask)
        if not answer:
            print ('no answer')
        
        diskbelow = str(answer[0])
        diskbelow = diskbelow[-5:]

        # find out what is currently at the top of new peg
        ask = parse_input("fact: (top ?X %s)" %newpeg)
        answer = self.kb.kb_ask(ask)
        topofnewpegdisk = ''
        if not answer:
            ask = parse_input("fact: (empty %s)" %newpeg)
            answer = self.kb.kb_ask(ask)
            if answer:
                topofnewpegdisk = 'base1'
        else:
            topofnewpegdisk = str(answer[0])
            topofnewpegdisk = topofnewpegdisk[-5:]

        # first we need to retract fact that the disk is at old peg
        statement1 = Statement(['on', disktomove, oldpeg])
        fact1 = Fact(statement1)

        # second, we need to assert fact that disk is on new peg
        statement2 = Statement(['on', disktomove, newpeg])
        fact2 = Fact(statement2)

        # third, assert that the target disk is on top of new peg 
        statement3 = Statement(['top', disktomove, newpeg])
        fact3 = Fact(statement3)
        
        # fourth, assert that diskbelow is the top of the old peg. or if there are no diskbelow, then declare old peg empty
        statement4 = ''
        if diskbelow == 'base1':
            statement4 = Statement(['empty', oldpeg])
        else:
            statement4 = Statement(['top', diskbelow, oldpeg])
        fact4 = Fact(statement4)

        # fifth, assert what the target disk is on top of now
        statement5 = Statement(['ontop', disktomove, topofnewpegdisk])
        fact5 = Fact(statement5)

        # sixth, retract the fact that the target disk is on top of diskbelow
        statement6 = Statement(['ontop', disktomove, diskbelow])
        fact6 = Fact(statement6)

        # need to retract the fact that top of new peg is top of new peg 
        statement7 = ''
        if topofnewpegdisk == 'base1': # if newpeg was empty, we need to RETRACT this fact 
            statement7 = Statement(['empty', newpeg])
        else: # if newpeg already has something, that something is no longer at the top 
            statement7 = Statement(['top', topofnewpegdisk, newpeg])
        fact7 = Fact(statement7)

        # eight, retract the fact the target disk is the top of old peg
        statement8 = Statement(['top', disktomove, oldpeg])
        fact8 = Fact(statement8)

        self.kb.kb_retract(fact1)
        self.kb.kb_retract(fact6)
        self.kb.kb_retract(fact7)
        self.kb.kb_retract(fact8)

        self.kb.kb_assert(fact2)
        self.kb.kb_assert(fact3)
        self.kb.kb_assert(fact4)
        self.kb.kb_assert(fact5)

        #print(self.kb)

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

        # enquire for Y = pos1
        ask1 = parse_input("fact: (YLOC ?tile pos1)")
        answers = self.kb.kb_ask(ask1)
        rows = [[0,0,0],[0,0,0],[0,0,0]]

        for i in range(1,4):
            p = str(i)
            currentrow = rows[i-1]
            ask1 = parse_input("fact: (YLOC ?tile pos%s)" %p)
            answers = self.kb.kb_ask(ask1)
            if not answers:
                print('error') 

            else:
                for answer in answers:
                    tile = str(answer)
                    tile = tile[-5:]
                    ask2 = parse_input("fact: (XLOC %s ?pos)" %tile) # find out its XPOS
                    answer = self.kb.kb_ask(ask2)
                    xpos = int((str(answer[0]))[-1])
                    if tile == 'empty':
                        currentrow[xpos-1] = -1
                    else:
                        currentrow[xpos-1] = int(tile[-1])

        # create the tuples from the lists
        row1 = tuple(rows[0])
        row2 = tuple(rows[1])
        row3 = tuple(rows[2])
        return (row1, row2, row3)

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
        terms = movable_statement.terms
        tile = terms[0].__str__()
        oldx = terms[1].__str__()
        oldy = terms[2].__str__()
        newx = terms[3].__str__()
        newy = terms[4].__str__()

        statement1 = Statement(['XLOC', tile, newx])
        fact1 = Fact(statement1)
        statement2 = Statement(['YLOC', tile, newy])
        fact2 = Fact(statement2)
        statement3 = Statement(['XLOC', 'empty', oldx])
        fact3 = Fact(statement3)
        statement4 = Statement(['YLOC', 'empty', oldy])
        fact4 = Fact(statement4)

        statement5 = Statement(['XLOC', tile, oldx])
        fact5 = Fact(statement5)
        statement6 = Statement(['YLOC', tile, oldy])
        fact6 = Fact(statement6)
        statement7 = Statement(['XLOC', 'empty', newx])
        fact7 = Fact(statement7)
        statement8 = Statement(['YLOC', 'empty', newy])
        fact8 = Fact(statement8)


        self.kb.kb_retract(fact5)
        self.kb.kb_retract(fact6)
        self.kb.kb_retract(fact7)
        self.kb.kb_retract(fact8)
        self.kb.kb_assert(fact1)
        self.kb.kb_assert(fact2)
        self.kb.kb_assert(fact3)
        self.kb.kb_assert(fact4)

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
