import random
import numpy as np

class Agent:
    def __init__(self):
        self.q_table = np.zeros((2047, 3))  # 2047 possible states, 3 possible actions (straight, right, left)
        self.epsilon = 1.0
        self.learning_rate = 0.1
        self.discount_factor = 0.9

    def state_to_index(self, state):
        # glue the values together into text, like "01000101001"
        binary_text = ""
        for value in state:
            binary_text += str(value)

        # read that text as a binary number -> page 0 to 2047
        return int(binary_text, 2)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            # explore: choose a random action
            return random.randint(0, 2)
        index = self.state_to_index(state)
        # exploit: choose the best action from Q-table
        scores = self.q_table[index]
        return int(np.argmax(scores))

    def learn(self, state, action, reward, next_state, game_over):
        index = self.state_to_index(state)
        next_index = self.state_to_index(next_state)
        old_score = self.q_table[index][action]
        if game_over:
            new_score = reward
        else:
            future_rewards = self.q_table[next_index]
            new_score = reward + self.discount_factor * np.max(future_rewards)
        new_score = (1 - self.learning_rate) * old_score + self.learning_rate * new_score
        self.q_table[index][action] = new_score
    def decay_epsilon(self):
        self.epsilon -= 0.001
        if self.epsilon < 0:
            self.epsilon = 0    


if __name__ == "__main__":
    agent = Agent()
    print(agent.state_to_index([1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0]))  # should print 578
    