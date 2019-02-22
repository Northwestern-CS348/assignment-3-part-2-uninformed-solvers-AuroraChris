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
        ### student code goes here


        output = ([],[],[])

        bindings_list = self.kb.kb_ask(parse_input('fact: (on ?disk ?peg)'))

        for binding in bindings_list:
            num1 = int(binding['?peg'][3])-1
            num2 = int(binding['?disk'][4])
            output[num1].append(num2)

        for index in output:
             index.sort()

        return tuple(tuple(e) for e in output)
        
        



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

        ### Student code goes here
        game_state = self.getGameState()
        
        disk = str(movable_statement.terms[0])
        old_peg = str(movable_statement.terms[1])
        new_peg = str(movable_statement.terms[2])

        old_peg_num = int(old_peg[-1])
        new_peg_num = int(new_peg[-1])


        if len(game_state[new_peg_num - 1]) == 0:
            retract = parse_input('fact: (empty ' + new_peg + ')')
            self.kb.kb_retract(retract)
            
        else:
            retract = parse_input('fact: (top disk' + str(game_state[new_peg_num - 1][0]) + ' ' + new_peg + ')')
            self.kb.kb_retract(retract)

        retract_1 = parse_input('fact: (on ' + disk + ' ' + old_peg + ')')
        retract_2 = parse_input('fact: (top ' + disk + ' ' + old_peg + ')')
        self.kb.kb_retract(retract_1)
        self.kb.kb_retract(retract_2)

        add_1 = parse_input('fact: (on ' + disk + ' ' + new_peg + ')')
        add_2 = parse_input('fact: (top ' + disk + ' ' + new_peg + ')')
        self.kb.kb_add(add_1)
        self.kb.kb_add(add_2)

        if len(game_state[old_peg_num - 1]) > 1:
            add = parse_input('fact: (top disk' + str(game_state[old_peg_num - 1][1]) + ' ' + old_peg + ')')
            self.kb.kb_add(add)
        else:
            add = parse_input('fact: (empty ' + old_peg + ')')
            self.kb.kb_add(add)

        

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
        
        output = []
        store = {}

        for y in range(1, 4):
            output1 = []

            for x in range(1, 4):

                ask = Fact(['on', '?tile', 'pos' + str(x), 'pos' + str(y)])
                bindingsList = self.kb.kb_ask(ask)

                if bindingsList != False:
                    for index in bindingsList:
                        if index['?tile'] not in store:

                            if index['?tile'] == 'empty':
                                store[index['?tile']] = -1

                            else:
                                tile_num = int(index['?tile'][-1])
                                store[index['?tile']] = tile_num

                        output1.append(store[index['?tile']])
                        # print(output1)
            # print(output1)
            output.append(tuple(output1))
        
        result = tuple(output)
        # print(result)


        return result
        
        

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


        tile = str(movable_statement.terms[0])
        old_x = str(movable_statement.terms[1])
        old_y = str(movable_statement.terms[2])
        new_x = str(movable_statement.terms[3])
        new_y = str(movable_statement.terms[4])

        retract_1 = parse_input('fact: (on ' + tile + ' ' + old_x + ' ' + old_y + ')')
        retract_2 = parse_input('fact: (on empty ' + new_x + ' ' + new_y + ')')
        self.kb.kb_retract(retract_1)
        self.kb.kb_retract(retract_2)

        add_1 = parse_input('fact: (on empty ' + old_x + ' ' + old_y + ')')
        add_2 = parse_input('fact: (on ' + tile + ' ' + new_x + ' ' + new_y + ')')
        self.kb.kb_add(add_1)
        self.kb.kb_add(add_2)


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
