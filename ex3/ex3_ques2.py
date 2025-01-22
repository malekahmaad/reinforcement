import random
import numpy as np
from tensorflow import keras


def r(choices):
    return random.choice(choices)

def main():
    sum = 0
    # Q = np.ndarray(shape=(22,2))
    episode_sums = []

    model = keras.Sequential()
    model.add(keras.layers.Dense(64, activation="relu"))
    model.add(keras.layers.Dense(32, activation='relu'))
    model.add(keras.layers.Dense(1, activation='linear'))
    model.compile(loss="mse")

    rewards = [i+1 for i in range(21)]
    choices = ["hit", "stay"]
    numbers = [i+1 for i in range(10)]
    for _ in range(100):
        R = np.zeros(shape=(1, 22))
        for i in range(1, 22):
            R[0][i] = random.choice(rewards)

        episode_sums.append(0)
        for _ in range(2):
            number = r(numbers)
            sum += number
            episode_sums.append(sum)

        while True:
            choice = r(choices)
            if choice == "stay":
                break
            number = r(numbers)
            sum += number
            episode_sums.append(sum)
            if sum > 21:
                break
        
        Y = np.zeros(shape=(1,))
        if sum > 21:
            Y[0] = 0
        else:
            Y[0] = R[0][sum-1]

        for i in range(len(episode_sums) - 1):
            s = episode_sums[i]
            OHE = np.zeros(shape=(1, 22))
            OHE[0][s] = 1
            X = np.hstack((OHE, R))
            # print(X)
            model.fit(X.astype('float32'), Y.astype("float32"))

        episode_sums = []
        sum = 0

    # for layer in model.layers:
    #     weights = layer.get_weights()
    #     print(f"Layer {layer.name} weights: {weights[0]}")
    #     print(f"Layer {layer.name} biases: {weights[1]}")
    episode_sums = []
    sum = 0
    encoded_states = []
    for _ in range(1000):
        R = np.zeros(shape=(1, 22))
        for i in range(1, 22):
            R[0][i] = random.choice(rewards)
        episode_sums.append(0)
        while True:
            OHE = np.zeros(shape=(1, 22))
            OHE[0][sum] = 1
            X = np.hstack((OHE, R))
            Q = model.predict(X.astype('float32'))
            # print(Q)
            if Q > R[0][sum]:
                encoded_states.append(X)
                number = r(numbers)
                sum += number
                episode_sums.append(sum)
            else:
                # print("minus Q")
                break

            if sum > 21:
                break
        
        Y = np.zeros(shape=(1,))
        if sum > 21:
            Y[0] = 0
        else:
            Y[0] = R[0][sum]

        for X in encoded_states:
            model.fit(X.astype('float32'), Y.astype('float32'))

        episode_sums = []
        sum = 0
        encoded_states = []

    episode_sums = []
    sum = 0
    reward = 0
    model_rewards = []
    for _ in range(100):
        R = np.zeros(shape=(1, 22))
        for i in range(1, 22):
            R[0][i] = random.choice(rewards)
        episode_sums.append(0)
        while True:
            OHE = np.zeros(shape=(1, 22))
            OHE[0][sum] = 1
            X = np.hstack((OHE, R))
            Q = model.predict(X.astype('float32'))
            # print(Q)
            if Q > R[0][sum]:
                number = r(numbers)
                sum += number
                episode_sums.append(sum)
            else:
                # print("minus Q")
                break

            if sum > 21:
                break

        if sum > 21:
            model_rewards.append(0)
        else:
            model_rewards.append(R[0][sum])
            reward += R[0][sum]

        episode_sums = []
        sum = 0

    # print(model_rewards, end="\n\n")
    print(f"AVG reward is: {reward/100}")


if __name__ == "__main__":
    main()