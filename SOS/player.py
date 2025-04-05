import SOS
import SOS_AI


def playerVSplayer():
    sos = SOS.SOS()
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
        if move == None:
            print("\033[91m" + "illegal move" + "\033[0m")

        print()
        print(sos)
        print(f"player 1 score is {sos.count1}")
        print(f"player 2 score is {sos.count2}", end="\n\n")

    if sos.status() == sos.player1:
        print("PLAYER 1 WINS")
    else:
        print("PLAYER 2 WINS")


def playerVSai():
    sos = SOS.SOS()
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
        print(sos)
        print(f"HUMAN score is {sos.count1}")
        print(f"AI score is {sos.count2}", end="\n\n")

    if sos.status() == sos.player1:
        print("HUMAN WINS")
    else:
        print("AI WINS")


def playerVSstrongAI():
    sos = SOS.SOS()
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
        print(sos)
        print(f"HUMAN score is {sos.count1}")
        print(f"AI score is {sos.count2}", end="\n\n")

    if sos.status() == sos.player1:
        print("HUMAN WINS")
    else:
        print("AI WINS")


def main():
    while True:
        choice = int(input("\nchoose an option:\n1-PLAYER VS PLAYER\n2-AI VS PLAYER\n3-STRONG AI VS PLAYER\nchoice:"))
        if choice == 1:
            playerVSplayer()
            break
        elif choice == 2:
            playerVSai()
            break
        elif choice == 3:
            playerVSstrongAI()
            break
    
if __name__ == "__main__":
    main()
