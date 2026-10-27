from snake_env import SnakeEnv  # type: ignore[reportMissingImports]
from agent import Agent
import matplotlib.pyplot as plt

env = SnakeEnv(width=20, height=20, render=False)
agent = Agent()
number_of_episodes = 3000
scores = []
amount_games = 0
average_score = 0
for game in range(number_of_episodes):
    state = env.reset()
    game_over = False
    while not game_over:
        action = agent.choose_action(state)
        next_state, reward, game_over = env.step(action)
        agent.learn(state, action, reward, next_state, game_over)
        state = next_state
    agent.decay_epsilon()
    scores.append(env.score)
    amount_games += 1
    average_score = (average_score * (amount_games - 1) + env.score) / amount_games

print(f"Average score over {number_of_episodes} episodes: {average_score}")
average_scores = []
for i in range(len(scores)):
    start = max(0, i - 19)
    last_games = scores[start:i + 1]
    average_scores.append(sum(last_games) / len(last_games))
plt.plot(scores, label="Score")
plt.plot(average_scores, color="red", label="Average (last 20)")
plt.xlabel("Game")
plt.ylabel("Score")
plt.title("Snake training")
plt.legend()
plt.show()