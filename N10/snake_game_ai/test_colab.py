import torch
import torch.nn as nn
import random
import os
import time
from train import SnakeNN, SnakeGame, GRID_WIDTH, GRID_HEIGHT
from IPython.display import display, HTML
from PIL import Image
import numpy as np

# Constants for game display
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Create a numpy array for the display using `IPython.display`
class ColabDisplay:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = np.zeros((height, width, 3), dtype=np.uint8)
        self.image_display = display("", display_id=True)

    def fill(self, color):
        self.surface[:] = color

    def rect(self, color, rect):
        x, y, w, h = rect
        self.surface[y:y+h, x:x+w] = color

    def show(self):
        img = Image.fromarray(self.surface)
        self.image_display.update(img)

# Display setup
DISPLAY = ColabDisplay(WIDTH, HEIGHT)
device = torch.device('cpu')

# Helper functions
def get_latest_checkpoint():
    checkpoints = [f for f in os.listdir('.') if f.startswith('snake_model_') and f.endswith('.pth')]
    if not checkpoints:
        return None
    latest_checkpoint = max(checkpoints, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    return latest_checkpoint

def load_model(filename):
    model = SnakeNN().to(device)
    model.load_state_dict(torch.load(filename, map_location=device))
    model.eval()
    return model

def render_game(game):
    DISPLAY.fill(BLACK)

    # Draw food
    DISPLAY.rect(RED, (game.food[0] * GRID_SIZE, game.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw snake
    for segment in game.snake.body:
        DISPLAY.rect(GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Display game state
    DISPLAY.show()
    print(f'Score: {game.snake.score}')

# Main function
def play_best_snake():
    model = None
    last_check_time = 0
    check_interval = 10
    latest_checkpoint = get_latest_checkpoint()

    if latest_checkpoint:
        print(f'Loading model from {latest_checkpoint}')
        model = load_model(latest_checkpoint)

    while True:
        current_time = time.time()
        if current_time - last_check_time > check_interval:
            new_checkpoint = get_latest_checkpoint()
            if new_checkpoint and new_checkpoint != latest_checkpoint:
                print(f'Loading model from {new_checkpoint}')
                model = load_model(new_checkpoint)
                latest_checkpoint = new_checkpoint
            last_check_time = current_time

        if model is None:
            print('No model found')
            time.sleep(5)
            continue

        game = SnakeGame()
        step_count = 0
        while True:
            state = game.get_state()
            with torch.no_grad():
                q_values = model(state)
            action = torch.argmax(q_values).item()

            game_over, _ = game.step(action)

            # Render the game every 3 steps
            if step_count % 3 == 0:
                render_game(game)
            step_count += 1

            if game_over:
                print(f'Game over! Score: {game.snake.score}')
                time.sleep(5)
                break

            time.sleep(0.1)  # Control game speed

if __name__ == '__main__':
    play_best_snake()
