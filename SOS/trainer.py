import SOS_AI
import SOS
import numpy as np
import time

def train_AI(iterations):
    network = SOS_AI.GameNetwork()
    network.model.compile(loss="mse")
    encoders = []
    policies = []
    for i in range(iterations):
        print(f"trining AI {i+1} times")
        game = SOS.SOS()
        AI1 = SOS_AI.MCTSPlayer()
        AI2 = SOS_AI.MCTSPlayer()
        while game.status() == -20:
            # print(game)
            # print(f"\n\n{game.legal_moves()}")
            # print("\nCurrent Player:", "RED" if game.player == game.RED else "YELLOW")
            if game.turn == game.player1:
                # print("entered\n")
                chosen_move = AI1.choose_move(game, 10000)
                root = AI1.root
                # print(chosen_move)
                row = chosen_move[0][0]
                column = chosen_move[0][1]
                char = chosen_move[1]

                game.make_move(char, row, column)
                
            else:
                # print("entered\n")
                chosen_move = AI2.choose_move(game, 10000)
                # print(chosen_move)
                root = AI2.root
                row = chosen_move[0][0]
                column = chosen_move[0][1]
                char = chosen_move[1]

                game.make_move(char, row, column)
                
            encoder = game.encode()
            encoders.append(encoder)
            policy = np.zeros(18)
            # value = game.status()
            sons = root.sons
            for son in sons:
                poisition = son.move[0][0] * 3 + son.move[0][1]
                policy[poisition] = son.n / root.n

            policy = policy.reshape(1, -1).astype(np.float32)
            policies.append(policy)
            # value = np.array([value]).reshape(1, -1).astype(np.float32)
        
        value = game.status()
        value = np.array([value]).reshape(1, -1).astype(np.float32)
        values = [value for _ in range(len(policies))]
        network.model.fit(encoders, [policies, values], epochs=1)

    network.save_weights()

start_time = time.time()
train_AI(1000)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")
