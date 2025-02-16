import random
import math

class ConnectFour:

    # Some constants that I want to use to fill the board.
    RED = 1
    YELLOW = -1
    EMPTY = 0

    # Game status constants
    RED_WIN = 1
    YELLOW_WIN = -1
    DRAW = 0
    ONGOING = -17  # Completely arbitrary

    def __init__(self):
        self.board = [[self.EMPTY for _ in range(6)] for _ in range(7)]
        self.heights = [0 for _ in range(7)]  # The column heights in the board.
        self.player = self.RED
        self.status = self.ONGOING

    def legal_moves(self):
        return [i for i in range(7) if self.heights[i] < 6]

    def make(self, move):  # Assumes that 'move' is a legal move
        self.board[move][self.heights[move]] = self.player
        self.heights[move] += 1
        # Check if the current move results in a winner:
        if self.winning_move(move):
            self.status = self.player
        elif len(self.legal_moves()) == 0:
            self.status = self.DRAW
        else:
            self.player = self.other(self.player)

    def other(self, player):
        return self.RED if player == self.YELLOW else self.YELLOW

    def unmake(self, move):
        self.heights[move] -= 1
        self.board[move][self.heights[move]] = self.EMPTY
        self.player = self.other(self.player)
        self.status = self.ONGOING

    def clone(self):
        clone = ConnectFour()
        clone.board = [col[:] for col in self.board]  # Deep copy columns
        clone.heights = self.heights[:]  # Deep copy heights
        clone.player = self.player
        clone.status = self.status
        return clone

    def winning_move(self, move):
        # Checks if the move that was just made wins the game.
        # Assumes that the player who made the move is still the current player.

        col = move
        row = self.heights[col] - 1  # Row of the last placed piece
        player = self.board[col][row]  # Current player's piece

        # Check all four directions: horizontal, vertical, and two diagonals
        # Directions: (dx, dy) pairs for all 4 possible win directions
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]   
        for dx, dy in directions:
            count = 0
            x, y = col + dx, row + dy
            while 0 <= x < 7 and 0 <= y < 6 and self.board[x][y] == player:
                count += 1
                x += dx
                y += dy
            x, y = col - dx, row - dy
            while 0 <= x < 7 and 0 <= y < 6 and self.board[x][y] == player:
                count += 1
                x -= dx
                y -= dy
            if count >= 3:
                return True
        return False

    def __str__(self):
        """
        Returns a string representation of the board.
        'R' for RED, 'Y' for YELLOW, '.' for EMPTY.
        """
        rows = []
        for r in range(5, -1, -1):  # From top row to bottom
            row = []
            for c in range(7):
                if self.board[c][r] == self.RED:
                    row.append("R")
                elif self.board[c][r] == self.YELLOW:
                    row.append("Y")
                else:
                    row.append(".")
            rows.append(" ".join(row))
        return "\n".join(rows)

class MCTSNode:
    def __init__(self, game, node, move):
        self.n = 1
        self.Q = 0
        self.son = None
        self.sons = []
        self.father = node
        self.game = game.clone()
        self.move = move

    def updateGame(self):
        self.game.make(self.move)

    def updateQ(self, r):
        self.Q = self.Q + (r - self.Q) / self.n

    def increase_n(self):
        self.n += 1

    def __str__(self):
        return f"Q = {self.Q}\nn = {self.n}\nmove = {self.move}"
    
    def greedy(self, sons):
        epsilon = 0.1
        prop = (epsilon, 1-epsilon)
        choices = [0, 1]
        choice = random.choices(choices, cum_weights=prop, k=1)[0]
        # print(choice)
        if choice == 0:
            self.son = random.choice(sons)
            # print(root.son)
                
        else:
            if self.game.player == self.game.RED:
                max = -2
                for son in sons:
                    if son.Q > max:
                        max = son.Q
                        self.son = son
                    
            else:
                min = 2
                for son in sons:
                    if son.Q < min:
                        min = son.Q
                        self.son = son

    def UCT(self):
        # Q_son + C sqrt((log N)/n_son)
        C = math.sqrt(2)
        if self.game.player == self.game.RED:
            max = float('-inf')
            for son in self.sons:
                v = son.Q + C * math.sqrt(math.log10(self.n)/son.n)
                if v > max:
                    max = v
                    self.son = son

        else:
            max = float('-inf')
            for son in self.sons:
                v = - son.Q + C * math.sqrt(math.log10(self.n)/son.n)
                if v > max:
                    max = v
                    self.son = son

        # print(self.son)


class MCTSPlayer:
    def select(self, node):
        curr_node = node
        # curr_node.increase_n()
        while len(curr_node.sons) == len(curr_node.game.legal_moves()):
            # print(len(curr_node.sons), len(curr_node.game.legal_moves()))
            curr_node.UCT()
            if curr_node.son == None:
                break
            curr_node = curr_node.son
            # curr_node.increase_n()

        return curr_node

    def expand(self, node):
        legal_moves = node.game.legal_moves()
        # moves = []
        for son in node.sons:
            if son.move in legal_moves:
                legal_moves.remove(son.move)

        # moves = legal_moves.difference(moves_done)
        # print(f"{legal_moves}")
        if legal_moves == []:
            return None
        move = random.choice(legal_moves)
        # print(move)
        x = MCTSNode(node.game, node, move)
        x.updateGame()
        node.sons.append(x)
        return x

    def rollout(self, game):
        newGame = game.clone()
        while newGame.status == newGame.ONGOING:
            legal_moves = newGame.legal_moves()
            move = random.choice(legal_moves)
            newGame.make(move)
        return newGame.status

    def backpropagate(self, node, result):
        node.Q = result
        curr_node = node.father
        while curr_node != None:
            curr_node.updateQ(result)
            curr_node.increase_n()
            curr_node = curr_node.father

    def choose_move(self, game, iterations):
        root = MCTSNode(game, None, None)
        # iter = 1
        for _ in range(iterations):
            # print(f"\nroot : {root}\n")
            node = self.select(root)
            # print(node)
            newNode = self.expand(node)
            if newNode != None:
                # print(newNode)
                result = self.rollout(newNode.game)
                # print(result)
                self.backpropagate(newNode, result)
                root.UCT()
        #     if root.game.status != game.ONGOING:
        #         break

        #     # print(f"iteration {iter}")
        #     # print(iter)
        #     # iter += 1
        #     legal_moves = game.legal_moves()
        #     sons = []
        #     for move in legal_moves:
        #         x = MCTSNode(game, root, move)
        #         x.updateGame()
        #         if x.game.status == game.ONGOING:
        #             q_list = [-1, 0, 1]
        #             x.Q = random.choice(q_list)
        #         else:
        #             x.Q = x.game.status
        #         root.increase_n()
        #         sons.append(x)
        #         root.updateQ(x.Q)
        #         # print(f"iteration {move}:")
        #         # print(f"root n is equal to {root.n}")
        #         # print(f"son q is equal to {x.Q}")
        #         # print(f"root q is equal to {root.Q}\n\n")

        #     if len(sons) == 1:
        #         root.son = sons[0]
        #         break

        #     else:
        #         root.UCT(sons)
        #         root = root.son              

        # while root.father != None:
        #     root = root.father

        return root.son.move


# Main function for debugging purposes: Allows two humans to play the game.
def main():
    """
    A simple main function for debugging purposes. 
    Allows two human players to play Connect Four in the terminal.
    """
    choice = int(input("choose game type:\n1- AI VS HUMAN\n2- AI VS AI\nyour choice:"))
    if choice == 1:
        game = ConnectFour()
        AI = MCTSPlayer()
        # newGame = game.clone()
        # game.make(1)
        # game.make(2)
        # game.make(1)
        # game.make(2)
        # game.make(1)
        # game.make(2)
        print("Welcome to Connect Four!")
        print("Player is RED (R) and AI is YELLOW (Y).\n")

        while game.status == game.ONGOING:
            print(game)
            # print(f"\n\n{game.legal_moves()}")
            print("\nCurrent Player:", "RED" if game.player == game.RED else "YELLOW")
            try:
                if game.player == game.RED:
                    move = int(input("Enter a column (0-6): "))
                    if move not in game.legal_moves():
                        print("Illegal move. Try again.")
                        continue
                    game.make(move)
                
                else:
                    chosen_move = AI.choose_move(game, 1000)
                    print(chosen_move)
                    game.make(chosen_move)
                # print(f"{game}\n\n")
                # game.unmake(move)
            except ValueError:
                print("Invalid input. Enter a number between 0 and 6.")
            except IndexError:
                print("Move out of bounds. Try again.")

        # print(newGame)
        # print("\n\n")
        print(game)
        if game.status == game.RED:
            print("\nRED (Player 1) wins!")
        elif game.status == game.YELLOW:
            print("\nYELLOW (Player 2) wins!")
        else:
            print("\nIt's a draw!")

    else:
        game = ConnectFour()
        AI1 = MCTSPlayer()
        AI2 = MCTSPlayer()
        # newGame = game.clone()
        # game.make(1)
        # game.make(2)
        # game.make(1)
        # game.make(2)
        # game.make(1)
        # game.make(2)
        print("Welcome to Connect Four!")
        print("AI 1 is RED (R) and AI 2 is YELLOW (Y).\n")

        while game.status == game.ONGOING:
            print(game)
            # print(f"\n\n{game.legal_moves()}")
            print("\nCurrent Player:", "RED" if game.player == game.RED else "YELLOW")
            try:
                if game.player == game.RED:
                    # print("entered\n")
                    chosen_move = AI1.choose_move(game, 1000)
                    # print(chosen_move)
                    game.make(chosen_move)
                
                else:
                    # print("entered\n")
                    chosen_move = AI2.choose_move(game, 1000)
                    # print(chosen_move)
                    game.make(chosen_move)
                # print(f"{game}\n\n")
                # game.unmake(move)
            except ValueError:
                print("Invalid input. Enter a number between 0 and 6.")
            except IndexError:
                print("Move out of bounds. Try again.")

        # print(newGame)
        # print("\n\n")
        print(game)
        if game.status == game.RED:
            print("\nRED (Player 1) wins!")
        elif game.status == game.YELLOW:
            print("\nYELLOW (Player 2) wins!")
        else:
            print("\nIt's a draw!")


if __name__ == "__main__":
    main()
