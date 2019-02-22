
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
        ### Student code goes here

        
        if not self.gm.isWon(): 
            movable_statement = self.gm.getMovables()

            if movable_statement != False:
                # print(movable_statement)
                for statement in movable_statement:
                    self.gm.makeMove(statement)

                    # GameState(state, depth, movableToReachThisState)
                    # deeper
                    state = self.gm.getGameState()
                    child = GameState(state, self.currentState.depth + 1, statement)
                    self.childState = child
                    self.childState.parent = self.currentState
                    self.currentState = self.childState
                    
                    if self.currentState in self.visited:
                        if self.visited[self.currentState] == True: 
                            self.reverse_helper(statement)
                            continue

                    else: 
                        self.visited[self.currentState] = True
                        break

            else:
                # print(self.currentState)
                statement = self.currentState.requiredMovable
                self.reverse_helper(statement)
                
                return False
                

        else: 
            return True

    def reverse_helper(self, statement):
        self.gm.reverseMove(statement)
        self.currentState = self.currentState.parent
        return

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
        
        if self.currentState.depth == 0:
            if len(self.currentState.children) == 0: 
                movable_statement = self.gm.getMovables()

                for statement in movable_statement: 
                    self.BFS_helper(statement, self.currentState)
        else:
            while self.currentState.parent:
                statement = self.currentState.requiredMovable
                self.reverse_helper(statement)



        while True:
            if len(self.currentState.children) - 1 < self.currentState.nextChildToVisit:
                return False
                
            else:

                next_child = self.currentState.children[self.currentState.nextChildToVisit]
                child_temp = self.currentState.children[self.currentState.nextChildToVisit]
                parent = child_temp.parent
                state = []

                self.currentState.nextChildToVisit += 1
                

                if next_child in self.visited and self.visited[next_child]: 
                    continue
                
                else:
                    

                    while True:
                        state.append(child_temp.requiredMovable)
                        child_temp = child_temp.parent
                        parent = child_temp.parent
                        if not parent:
                            break

                    state.reverse()
                    for statement in state:
                        self.gm.makeMove(statement)

                    self.visited[next_child] = True

                    if not self.gm.isWon(): 
                        movable_statement = self.gm.getMovables()
                        
                        for statement in movable_statement: 
                            self.BFS_helper(statement, next_child)

                        self.currentState = next_child
                        return False
                    
                    else:
                        return True

    def reverse_helper(self, statement):
        self.gm.reverseMove(statement)
        self.currentState = self.currentState.parent
        return   
                

    def BFS_helper(self, statement, state):
        depth = state.depth + 1
        self.gm.makeMove(statement)
        newState = self.gm.getGameState()
        child = GameState(newState, depth, statement)
        child.parent = state
        self.currentState.children.append(child)
        self.gm.reverseMove(statement)
        return
