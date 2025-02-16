import random
import math
from tensorflow import keras


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
        self.game.make_move(self.move[1], self.move[0][0], self.move[0][1])

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
            if self.game.turn == self.game.player1:
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
        if self.game.turn == self.game.player1:
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
    def __init__(self):
        self.root = None

    def select(self, node):
        # print(node.game)
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
        while newGame.status() == -20:
            legal_moves = newGame.legal_moves()
            move = random.choice(legal_moves)
            newGame.make_move(move[1], move[0][0], move[0][1])
        return newGame.status()

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

        self.root = root
        return root.son.move
    
class GameNetwork:
    def __init__(self):
        length = 3 * 3
        input_layer = keras.Input(shape = ((2 * length) + 3,))
        
        x = keras.layers.Dense(64, activation="relu")(input_layer)
        x = keras.layers.Dense(64, activation="relu")(x)

        policy_logits = keras.layers.Dense(2 * length, activation=None)(x)
        policy_output = keras.layers.Softmax(name="policy_output")(policy_logits)

        value_output = keras.layers.Dense(1, activation="tanh", name="value_output")(x)

        self.model = keras.Model(inputs=input_layer, outputs=[policy_output, value_output], name="SOS_network")

    def save_weights(self):
        self.model.save_weights("SOS.weights.h5", overwrite=True)

    def load_weights(self):
        self.model.load_weights("SOS.weights.h5", skip_mismatch=False)


class PUCTNode:
    def __init__(self, game, node, move):
        self.mctsNode = MCTSNode(game, node, move)
        self.P = 0

    def updateP(self, newP):
        self.P = newP

    def UCT(self):
        # son.Q + C * son.P * math.sqrt(father.n) / (1 + son.n)
        C = math.sqrt(2)
        if self.mctsNode.game.turn == self.mctsNode.game.player1:
            max = float('-inf')
            for son in self.mctsNode.sons:
                U = son.mctsNode.Q + C * son.P * math.sqrt(son.mctsNode.father.mctsNode.n) / (1 + son.mctsNode.n)
                if U > max:
                    max = U
                    self.mctsNode.son = son

        else:
            max = float('-inf')
            for son in self.mctsNode.sons:
                U = - son.mctsNode.Q + C * son.P * math.sqrt(son.mctsNode.father.mctsNode.n) / (1 + son.mctsNode.n)
                if U > max:
                    max = U
                    self.mctsNode.son = son


class PUCTPlayer:
    def __init__(self):
        self.network = GameNetwork()
        self.network.load_weights()

    def select(self, node):
        # print(node.game)
        curr_node = node
        # curr_node.increase_n()
        while len(curr_node.mctsNode.sons) == len(curr_node.mctsNode.game.legal_moves()):
            # print(len(curr_node.sons), len(curr_node.game.legal_moves()))
            curr_node.UCT()
            if curr_node.mctsNode.son == None:
                break
            curr_node = curr_node.mctsNode.son
            # curr_node.increase_n()

        return curr_node

    def expand(self, node):
        legal_moves = node.mctsNode.game.legal_moves()
        # moves = []
        for son in node.mctsNode.sons:
            if son.mctsNode.move in legal_moves:
                legal_moves.remove(son.mctsNode.move)

        # moves = legal_moves.difference(moves_done)
        # print(f"{legal_moves}")
        if legal_moves == []:
            return None
        move = random.choice(legal_moves)
        # print(move)
        x = PUCTNode(node.mctsNode.game, node, move)
        encoder = node.mctsNode.game.encode()
        prediction = self.network.model.predict(encoder)
        probs = prediction[0][0]
        # self.move[0][0], self.move[0][1]
        position = move[0][0] * 3 + move[0][1]
        x.updateP(probs[position])
        x.mctsNode.updateGame()
        node.mctsNode.sons.append(x)
        return x

    def rollout(self, game):
        encoder = game.encode()
        prediction = self.network.model.predict(encoder)
        return prediction[1][0][0]

    def backpropagate(self, node, result):
        node.mctsNode.Q = result
        curr_node = node.mctsNode.father
        while curr_node != None:
            curr_node.mctsNode.updateQ(result)
            curr_node.mctsNode.increase_n()
            curr_node = curr_node.mctsNode.father

    def choose_move(self, game, iterations):
        root = PUCTNode(game, None, None)
        # iter = 1
        for _ in range(iterations):
            # print(f"\nroot : {root}\n")
            node = self.select(root)
            # print(node)
            newNode = self.expand(node)
            # print(newNode.mctsNode.father)
            if newNode != None:
                # print(newNode)
                result = self.rollout(newNode.mctsNode.game)
                # print(result)
                self.backpropagate(newNode, result)
                root.UCT()

        return root.mctsNode.son.mctsNode.move
    