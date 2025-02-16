import random
import numpy as np

def r(choices):
    return random.choice(choices)


def epsilon_greedy(hit, stay):
    epsilon = 0.1
    prop = (epsilon, 1-epsilon)
    choices = [0, 1]
    choice = random.choices(choices, cum_weights=prop, k=1)[0]
    # print(choice)
    if choice == 0:
        choices_hit = ["hit", "stay"]
        return r(choices_hit)
    else:
        if hit > stay:
            return "hit"
        return "stay"

def main():
    sum = 0
    Q = np.zeros(shape=(22, 3))
    for i in range(22):
        Q[i][2] = i

    episode_sums = []
    choices = ["hit", "stay"]
    numbers = [i+1 for i in range(10)]
    for _ in range(100):
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

        # print(episode_sums, end="\n\n")
        for i in range(len(episode_sums) - 1):
            s = episode_sums[i]
            if sum <= 21:
                n = Q[s][1]
                Q[s][0] += (1 / (n + 1)) * (sum - Q[s][0])
                Q[s][1] += 1
            else:
                Q[s][1] += 1

        # if  np.isnan(Q).sum() > 0 :
        #     print(episode_sums)

        episode_sums = []
        sum = 0

    for _ in range(1000):
        episode_sums.append(0)
        while True:
            choice = epsilon_greedy(Q[sum][0], Q[sum][2])
            if choice == "stay":
                break
            number = r(numbers)
            sum += number
            episode_sums.append(sum)
            if sum > 21:
                break
            
        for i in range(len(episode_sums) - 1):
            s = episode_sums[i]
            if sum <= 21:
                n = Q[s][1]
                Q[s][0] += (1 / (n + 1)) * (sum - Q[s][0])
                Q[s][1] += 1
            else:
                Q[s][1] += 1

        episode_sums = []
        sum = 0

    # print(Q)
    # print(Q[:,0].mean())

    reward = 0
    for _ in range(100):
        episode_sums.append(0)
        while True:
            # choice = "stay"
            # if Q[sum][0] > Q[sum][2]:
            #     choice = "hit"
            choice = epsilon_greedy(Q[sum][0], Q[sum][2])
            if choice == "stay":
                break
            number = r(numbers)
            sum += number
            episode_sums.append(sum)
            if sum > 21:
                break
        
        # print(sum)
        # print(reward)
        # print("\n\n")
        if sum <= 21:
            reward += sum 

        episode_sums = []
        sum = 0      
        
    print(reward / 100)


if __name__ == "__main__":
    main()