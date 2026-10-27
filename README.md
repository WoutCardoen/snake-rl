# Snake RL
One sentence: a Q-learning agent that learns to play Snake, built with Pygame.

## How it works
- **State:** what does the agent "see"? (e.g. danger ahead/left/right, food direction, current direction)
- **Actions:** what can it do? (straight / left / right?)
- **Rewards:** what does it get for eating food, dying, or a normal step?
- **Learning:** Q-table, plus your learning rate, discount factor and how epsilon decays.

## Files
- `snake_env.py`: the game environment
- `agent.py`: the Q-learning agent
- `train.py`: training loop

## Run it
pip install -r requirements.txt
python train.py

## Results
What score does it reach after X games? (A matplotlib plot or GIF here is a nice touch.)