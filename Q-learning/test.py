import random
import numpy as np
from tensorflow import keras

# Hyperparameters
EPISODES = 200
GAMMA = 0.99
EPSILON = 1.0
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.01

# Neural Network
model = keras.Sequential([
    keras.layers.Dense(128, activation="relu", input_shape=(43,)),
    keras.layers.Dense(256, activation="relu"),
    keras.layers.Dense(256, activation="relu"),
    keras.layers.Dense(1, activation="linear")  # Q-value for "hit"
])
model.compile(optimizer="adam", loss="mse")

# Helper Functions
def get_state(sum, rewards):
    OHE = np.zeros(22)
    OHE[sum-1] = 1
    return np.hstack((OHE, rewards)).reshape(1, -1)

def choose_action(state, epsilon):
    if np.random.rand() < epsilon:
        return random.choice(["hit", "stay"])
    else:
        q_value = model.predict(state, verbose=0)
        return "hit" if q_value > 0 else "stay"

# Training
for episode in range(EPISODES):
    rewards = np.random.randint(1, 22, size=21)
    sum = 0
    state = get_state(sum, rewards)
    episode_history = []

    while True:
        action = choose_action(state, EPSILON)
        if action == "stay":
            break
        number = random.randint(1, 10)
        sum += number
        if sum <= 21: 
            next_state = get_state(sum, rewards)
            episode_history.append((state, action, sum))
            state = next_state
        if sum > 21:
            break

    print("entered")
    # Update Q-values using Bellman equation
    for state, action, sum in episode_history:
        target = rewards[sum-1] if sum <= 21 else 0
        if action == "hit":
            target += GAMMA * model.predict(get_state(sum, rewards), verbose=0)
        model.fit(state, np.array([[target]]), verbose=0)

    # Decay epsilon
    EPSILON = max(MIN_EPSILON, EPSILON * EPSILON_DECAY)

# Evaluation
total_rewards = 0
for _ in range(100):
    rewards = np.random.randint(1, 22, size=21)
    sum = 0
    state = get_state(sum, rewards)
    while True:
        action = choose_action(state, 0)
        if action == "stay":
            total_rewards += rewards[sum]
            break
        number = random.randint(1, 10)
        sum += number
        if sum <= 21:
            state = get_state(sum, rewards)
        if sum > 21:
            break

print(f"Average reward: {total_rewards / 100}")