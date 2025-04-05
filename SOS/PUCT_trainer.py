import SOS_AI
import SOS
import numpy as np
import time

size = 5
number_of_games = 10000
PUCT_iterations = 10000

def train_PUCT_AI(iterations):
    network = SOS_AI.GameNetwork()
    network.model.compile(loss="mse")
    for i in range(iterations):
        print(f"training PUCT AI {i+1} times")
        game = SOS.SOS()
        PUCT_AI = SOS_AI.PUCTPlayer()
        encoders = []
        policies = []
        while game.status() == -20:
            chosen_move = PUCT_AI.choose_move(game, PUCT_iterations)
            root = PUCT_AI.root
            row = chosen_move[0][0]
            column = chosen_move[0][1]
            char = chosen_move[1]
            game.make_move(char, row, column)
                
            encoder = game.encode()
            encoders.append(encoder)
            policy = np.zeros(2 * size * size)
            sons = root.sons
            for son in sons:
                if son.move[1] == "S":
                    position = son.move[0][0] * size + son.move[0][1]
                else:
                    position = son.move[0][0] * size + son.move[0][1] + (size * size)

                policy[position] = son.n / root.n

            policy = policy.reshape(1, -1).astype(np.float32)
            policies.append(policy)
        
        value = game.status()
        value = np.array([value]).reshape(1, -1).astype(np.float32)
        
        encoders = np.array(encoders, dtype=np.float32).reshape(-1, (size * size * 2) + 3)
        policies = np.array(policies, dtype=np.float32)
        values = np.full((len(encoders), 1), value, dtype=np.float32)
        network.model.fit(encoders, [policies, values], epochs=1)

    network.save_weights()

start_time = time.time()
train_PUCT_AI(number_of_games)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")
