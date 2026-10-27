import random
import pygame

RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)
UP = (0, -1)
CLOCKWISE = [RIGHT, DOWN, LEFT, UP]

class SnakeEnv:
    def __init__(self, width=20, height=20, render=False):
        self.width = width
        self.height = height
        self.render = render
        if self.render:
            pygame.init()
            self.cell_size = 20
            self.screen = pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))
            pygame.display.set_caption("Snake Game")
            self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = random.choice(CLOCKWISE)
        self.food = self.place_food()
        self.done = False
        self.steps = 0
        self.score = 0
        return self._get_observation()

    def draw(self):
    # keep the window responsive, and let the X button close it
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.screen.fill((0, 0, 0))   # black background
        for x, y in self.snake:
            rect = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (0, 200, 0), rect)   # green snake
        fx, fy = self.food
        rect = (fx * self.cell_size, fy * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, (200, 0, 0), rect)       # red food

        pygame.display.flip()   # show what we drew
        self.clock.tick(10)     # max 10 moves per second

    def place_food(self):
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake:
                return food
            
    def turn(self, action):
        idx = CLOCKWISE.index(self.direction)
        if action == 0:  # straight
            new_idx = idx
        elif action == 1:  # right
            new_idx = (idx + 1) % 4
        elif action == 2:  # left
            new_idx = (idx - 1) % 4
        self.direction = CLOCKWISE[new_idx]

    def is_collision(self, position):
        x, y = position
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        if position in self.snake[1:]:  
            return True
        return False
            
    def step(self, action):
        if self.done:
            raise Exception("Game is over, call reset() first")
        self.steps += 1
        self.turn(action)
        # where the head ends up after this move
        x, y = self.snake[0]
        dx, dy = self.direction
        new_head = (x + dx, y + dy)
        # hit something, or wandering around too long without eating
        if self.is_collision(new_head) or self.steps > 100 * len(self.snake):
            self.done = True
            return self._get_observation(), -10, True
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.steps = 0
            self.food = self.place_food()
            reward = 10
        else:
            # didn't eat, so drop the tail to keep the same length
            self.snake.pop()
            reward = 0
        if self.render:
            self.draw()
        return self._get_observation(), reward, False

    def _get_observation(self):
        moving_up = self.direction == UP
        moving_down = self.direction == DOWN
        moving_left = self.direction == LEFT
        moving_right = self.direction == RIGHT

        head_x, head_y = self.snake[0]
        food_x, food_y = self.food

        food_up = food_y < head_y
        food_down = food_y > head_y
        food_left = food_x < head_x
        food_right = food_x > head_x

        idx = CLOCKWISE.index(self.direction)
        dir_straight = CLOCKWISE[idx]
        dir_right = CLOCKWISE[(idx + 1) % 4]
        dir_left = CLOCKWISE[(idx - 1) % 4]
        cell_straight = (head_x + dir_straight[0], head_y + dir_straight[1])
        cell_right = (head_x + dir_right[0], head_y + dir_right[1])
        cell_left = (head_x + dir_left[0], head_y + dir_left[1])
        danger_straight = self.is_collision(cell_straight)
        danger_right = self.is_collision(cell_right)
        danger_left = self.is_collision(cell_left)

        state = [
            danger_straight, danger_right, danger_left,
            moving_up, moving_down, moving_left, moving_right,
            food_up, food_down, food_left, food_right,
        ]
        return [int(value) for value in state]
    
if __name__ == "__main__":
    env = SnakeEnv(width=20, height=20, render=True)
    game_over = False
    while not game_over:
        action = random.randint(0, 2)
        state, reward, game_over = env.step(action)
        print("action:", action, "head:", state, "reward:", reward)
    print("Score:", env.score)