import pygame
import torch
import torch.nn as nn   
import random
import os
import time
from train import SnakeNN, SnakeGame, GRID_WIDTH, GRID_HEIGHT

pygame.init()

WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255)
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')

def get_latest_checkpoint():
    checkpoints = [f for f in os.listdir('.') if f.startswith('snake_model_') and f.endswith('.pth')]
    if not checkpoints:
        return None
    latest_checkpoint = max(checkpoints, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    return latest_checkpoint

def load_model(filename):
    model = SnakeNN().to(device)
    #model.load_state_dict(torch.load(filename))
    model.load_state_dict(torch.load(filename, map_location=device))
    model.eval()
    return model

def render_game(game):
    DISPLAY.fill(BLACK)

    pygame.draw.rect(DISPLAY, RED, (game.food[0] * GRID_SIZE, game.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    for segment in game.snake.body:
        pygame.draw.rect(DISPLAY, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {game.snake.score}', True, WHITE)
    DISPLAY.blit(text, (10, 10))

    pygame.display.flip()

def play_best_snake():
    model = None
    clock = pygame.time.Clock()
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
            pygame.time.wait(5000)
            continue

        game = SnakeGame()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            state = game.get_state()
            with torch.no_grad():
                q_values = model(state)
            action = torch.argmax(q_values).item()

            game_over, _ = game.step(action)

            render_game(game)

            if game_over:
                print(f'Game over! Score: {game.snake.score}')
                pygame.time.wait(5000)
                break

            clock.tick(100)

if __name__ == '__main__':  
    play_best_snake()