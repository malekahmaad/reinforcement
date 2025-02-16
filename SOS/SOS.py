import numpy as np
import SOS_AI

size = 3

class SOS:
    S = 1
    O = -1
    EMPTY = 0

    player1 = 1
    player2 = -1


    def __init__(self):
        self.board = []
        for _ in range(size):
            row = []
            for _ in range(size):
                row.append(self.EMPTY)

            self.board.append(row)

        self.count1 = 0
        self.count2 = 0
        self.turn = self.player1


    def make_move(self, char, row, column):
        if row < 0 or row > size - 1 or column < 0 or column > size - 1:
            return None
        
        if self.board[row][column] != self.EMPTY:
            return None

        SOS_counter = 0
        if char.upper() == "S":
            self.board[row][column] = self.S
            if 0 <= row <= size - 1 and 0 <= column <= size - 3:
                if self.board[row][column + 1] == self.O and self.board[row][column + 2] == self.S:
                    SOS_counter += 1

            if 0 <= column <= size - 1 and 0 <= row <= size - 3:
                if self.board[row + 1][column] == self.O and self.board[row + 2][column] == self.S:
                    SOS_counter += 1

            if 0 <= row <= size - 1 and 2 <= column <= size - 1:
                if self.board[row][column - 1] == self.O and self.board[row][column - 2] == self.S:
                    SOS_counter += 1

            if 0 <= column <= size - 1 and 2 <= row <= size - 1:
                if self.board[row - 1][column] == self.O and self.board[row - 2][column] == self.S:
                    SOS_counter += 1

            if 0 <= row <= size - 3 and 0 <= column <= size - 3:
                if self.board[row + 1][column + 1] == self.O and self.board[row + 2][column + 2] == self.S:
                    SOS_counter += 1

            if 0 <= row <= size - 3 and 2 <= column <= size - 1:
                if self.board[row + 1][column - 1] == self.O and self.board[row + 2][column - 2] == self.S:
                    SOS_counter += 1
            
            if 2 <= row <= size - 1 and 0 <= column <= size - 3:
                if self.board[row - 1][column + 1] == self.O and self.board[row - 2][column + 2] == self.S:
                    SOS_counter += 1

            if 2 <= row <= size - 1 and 2 <= column <= size - 1:
                if self.board[row - 1][column - 1] == self.O and self.board[row - 2][column - 2] == self.S:
                    SOS_counter += 1

        elif char.upper() == "O":
            self.board[row][column] = self.O
            if 0 <= row <= size - 1 and 0 < column < size - 1:
                if self.board[row][column - 1] == self.S and self.board[row][column + 1] == self.S:
                    SOS_counter += 1

            if 0 <= column <= size - 1 and 0 < row < size - 1:
                if self.board[row - 1][column] == self.S and self.board[row + 1][column] == self.S:
                    SOS_counter += 1
            
            if row > 0 and row < size - 1 and column > 0 and column < size - 1:
                if self.board[row - 1][column - 1] == self.S and self.board[row + 1][column + 1] == self.S:
                    SOS_counter += 1
                    
                if self.board[row - 1][column + 1] == self.S and self.board[row + 1][column - 1] == self.S:
                    SOS_counter += 1

        else:
            return None

        if self.turn == self.player1:
            self.count1 += SOS_counter

        else:
            self.count2 += SOS_counter

        if SOS_counter == 0:
            self.turn *= -1

        return 1


    def unmake_move(self, row, column):
        self.board[row][column] = self.EMPTY
        self.turn *= -1


    def clone(self):
        newGame = SOS()
        newGame.board = [row[:] for row in self.board]
        newGame.count1 = self.count1
        newGame.count2 = self.count2
        newGame.turn = self.turn
        return newGame   

    def status(self):
        if len(self.legal_moves()) == 0:
            if self.count1 > self.count2:
                return self.player1
            elif self.count1 < self.count2:
                return self.player2
            else:
                return 0
            
        return -20

    
    def legal_moves(self):
        moves = []
        for i in range(size):
            for j in range(size):
                if self.board[i][j] == self.EMPTY:
                    moves.append(((i, j), "S"))
                    moves.append(((i, j), "O"))

        return moves
    

    def encode(self):
        binary = np.zeros(shape=(1,(size*size)*2 + 3))
        count = 0
        for i in range(size):
            for j in range(size):
                if self.board[i][j] == self.S:
                    binary[0][count] = 1
                count += 1

        for i in range(size):
            for j in range(size):
                if self.board[i][j] == self.O:
                    binary[0][count] = 1
                count += 1

        binary[0][count] = self.count1
        binary[0][count + 1] = self.count2
        binary[0][count + 2] = self.turn
        # print(binary)
        return binary

    
    def decode(self, actions):
        max_index = 0
        for i in range(1, size*size*2):
            if actions[i] > actions[max_index]:
                max_index = i

        if max_index < size * size:
            char = 's'
        else:
            char = 'o'
            max_index -= (size * size)

        row = max_index // size
        column = max_index % size 
        return row, column, char
    

    def __str__(self):
        game_board = ""
        for i in range(size):
            for j in range(size):
                if self.board[i][j] == self.S:
                    game_board += "S "
                elif self.board[i][j] == self.O:
                    game_board += "O "
                else:
                    game_board += "_ "

            game_board += "\n"

        return game_board

def playerVSplayer():
    sos = SOS()
    network = SOS_AI.GameNetwork()
    print(sos)
    print(f"player 1 score is {sos.count1}")
    print(f"player 2 score is {sos.count2}", end="\n\n")
    while sos.status() == -20:
        if sos.turn == sos.player1:
            print("PLAYER 1 turn: ")
        else:
            print("PLAYER 2 turn: ")
        row = int(input("choose a row: "))
        column = int(input("choose a column: "))
        char = input("choose a S or O: ")
        move = sos.make_move(char, row, column)
        encoder = sos.encode()
        # print(encoder.shape)
        prediction = network.model.predict(encoder)
        print(prediction[1][0][0])
        # weights = network.model.get_weights()
        # print(weights)
        # network.save_weights()
        # network.load_weights()
        # weights = network.model.get_weights()
        # print(weights)
        # print(sos.decode(prediction[0][0]))
        if move == None:
            print("\033[91m" + "illegal move" + "\033[0m")

        print()
        # print(sos.status())
        print(sos)
        print(f"player 1 score is {sos.count1}")
        print(f"player 2 score is {sos.count2}", end="\n\n")

    if sos.status() == sos.player1:
        print("PLAYER 1 WINS")
    else:
        print("PLAYER 2 WINS")


def playerVSai():
    sos = SOS()
    AI = SOS_AI.MCTSPlayer()
    print(sos)
    print(f"player 1 score is {sos.count1}")
    print(f"player 2 score is {sos.count2}", end="\n\n")
    while sos.status() == -20:
        if sos.turn == sos.player1:
            print("PLAYER 1 turn: ")
            row = int(input("choose a row: "))
            column = int(input("choose a column: "))
            char = input("choose a S or O: ")
        else:
            # print(type(sos))
            print("AI turn: ")
            print("AI thinking...")
            move = AI.choose_move(sos, 20000)
            row = move[0][0]
            column = move[0][1]
            char = move[1]

        move = sos.make_move(char, row, column)
        if move == None:
            print("\033[91m" + "illegal move" + "\033[0m")

        print()
        # print(sos.encode())
        print(sos)
        print(f"HUMAN score is {sos.count1}")
        print(f"AI score is {sos.count2}", end="\n\n")

    if sos.status() == sos.player1:
        print("HUMAN WINS")
    else:
        print("AI WINS")


def playerVSstrongAI():
    sos = SOS()
    AI = SOS_AI.PUCTPlayer()
    print(sos)
    print(f"player 1 score is {sos.count1}")
    print(f"player 2 score is {sos.count2}", end="\n\n")
    while sos.status() == -20:
        if sos.turn == sos.player1:
            print("PLAYER 1 turn: ")
            row = int(input("choose a row: "))
            column = int(input("choose a column: "))
            char = input("choose a S or O: ")
        else:
            # print(type(sos))
            print("AI turn: ")
            print("AI thinking...")
            move = AI.choose_move(sos, 10000)
            row = move[0][0]
            column = move[0][1]
            char = move[1]

        move = sos.make_move(char, row, column)
        if move == None:
            print("\033[91m" + "illegal move" + "\033[0m")

        print()
        # print(sos.encode())
        print(sos)
        print(f"HUMAN score is {sos.count1}")
        print(f"AI score is {sos.count2}", end="\n\n")

    if sos.status() == sos.player1:
        print("HUMAN WINS")
    else:
        print("AI WINS")

# playerVSai()
# playerVSplayer()
playerVSstrongAI()
