import random
import torch
import torch.nn as nn
import torch.optim as optim 
from collections import deque
import torch.cuda.amp as amp
import itertools
import json

GRID_WIDTH = 20
GRID_HEIGHT = 20

#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#print(f'Using device: {device}')
device = torch.device("cpu")

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.score += 1
        self.body.append(self.body[-1])

    def check_collision(self):
        head = self.body[0]
        return (
            head[0] < 0
            or head[0] >= GRID_WIDTH
            or head[1] < 0
            or head[1] >= GRID_HEIGHT
            or head in self.body[1:]
        )
    
class SnakeNN(nn.Module):
    def __init__(self):
        super(SnakeNN, self).__init__()
        self.fc1 = nn.Linear(26, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 4)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        return self.fc4(x)
    
class SnakeGame:
    def __init__(self):
        self.snake = Snake()
        self.food = self.spawn_food()
        self.steps_without_food = 0
        self.max_steps_without_food = GRID_WIDTH * GRID_HEIGHT

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake.body:
                return food
    
    def step(self, action):
        direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.snake.direction = direction[action]

        self.snake.move()
        self.steps_without_food += 1

        game_over = False
        if self.snake.body[0] == self.food:
            self.snake.grow()
            self.food = self.spawn_food()
            self.steps_without_food = 0
            reward = 10
        elif self.steps_without_food >= self.max_steps_without_food:
            game_over = True
            reward = -10
        elif self.snake.check_collision():
            game_over = True
            reward = -10
        else:
            reward = -0.1
        return game_over, reward
    
    def get_state(self):
        head = self.snake.body[0]
        state = [
            int(self.snake.direction == (0, 1)),
            int(self.snake.direction == (0, -1)),
            int(self.snake.direction == (1, 0)),
            int(self.snake.direction == (-1, 0)),

            int(head[1] < self.food[1]),
            int(head[1] > self.food[1]),
            int(head[0] < self.food[0]),
            int(head[0] > self.food[0]),
            
            int(head[1] == 0 or (head[0], head[1] - 1) in self.snake.body),
            int(head[1] == GRID_HEIGHT - 1 or (head[0], head[1] + 1) in self.snake.body),
            int(head[0] == GRID_WIDTH - 1 or (head[0] + 1, head[1]) in self.snake.body),
            int(head[0] == 0 or (head[0] - 1, head[1]) in self.snake.body),

            abs(head[0] - self.food[0]) / GRID_WIDTH,
            abs(head[1] - self.food[1]) / GRID_HEIGHT,

            len(self.snake.body) / (GRID_WIDTH * GRID_HEIGHT),

            self.steps_without_food / self.max_steps_without_food,

            int(self.snake.body[-1][0] < head[0]),
            int(self.snake.body[-1][0] > head[0]),
            int(self.snake.body[-1][1] < head[1]),
            int(self.snake.body[-1][1] > head[1]),

            self.snake.score / 100,
            (GRID_WIDTH * GRID_HEIGHT - len(self.snake.body)) / (GRID_WIDTH * GRID_HEIGHT),
            int(len(self.snake.body) > 1 and self.snake.body[1] == (head[0], head[1] - 1)),
            int(len(self.snake.body) > 1 and self.snake.body[1] == (head[0], head[1] + 1)),
            int(len(self.snake.body) > 1 and self.snake.body[1] == (head[0] + 1, head[1])),
            int(len(self.snake.body) > 1 and self.snake.body[1] == (head[0] - 1, head[1])),
        ]
        return torch.tensor(state, dtype=torch.float32).to(device)

def save_model(model, filename):
    torch.save(model.state_dict(), filename)

def load_model(filename):
    model = SnakeNN().to(device)
    #model.load_state_dict(torch.load(filename))
    model.load_state_dict(torch.load(filename, map_location=device))
    return model

def train(checkpoint_path=None):
    if checkpoint_path:
        model = load_model(checkpoint_path)
        print(f'Loaded model from {checkpoint_path}')
    else:
        model = SnakeNN().to(device)

    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    scaler = amp.GradScaler()
    epsilon = 1.0
    scores = []
    total_rewards = []
    memory = deque(maxlen=100000)

    batch_size = 16384
    print(f'Batch size: {batch_size}')
    gamma = 0.99
    epsilon_decay = 0.9997
    epsilon_min = 0.01

    num_episodes = 500000
    max_steps = 5000
    train_frequency = 5

    for episode in range(num_episodes):
        game = SnakeGame()
        state = game.get_state()
        total_reward = 0
        steps = 0

        while steps < max_steps:
            steps += 1
            if random.random() < epsilon:
                action = random.randint(0, 3)
            else:
                with torch.no_grad():
                    q_values = model(state.unsqueeze(0))
                    action = torch.argmax(q_values).item()

            game_over, reward = game.step(action)
            next_state = game.get_state()
            total_reward += reward

            memory.append((state, action, reward, next_state, game_over))
            state = next_state

            if game_over:
                break

        scores.append(game.snake.score)
        total_rewards.append(total_reward)

        if episode % train_frequency == 0 and len(memory) > batch_size:
            batch = random.sample(memory, batch_size)
            states, actions, rewards, next_states, dones = zip(*batch)

            states = torch.stack(states).to(device)
            actions = torch.tensor(actions, dtype=torch.long).unsqueeze(1).to(device)
            rewards = torch.tensor(rewards, dtype=torch.float32).to(device)
            next_states = torch.stack(next_states).to(device)
            dones = torch.tensor(dones, dtype=torch.float32).to(device)

            with amp.autocast():
                current_q = model(states).gather(1, actions)
                next_q = model(next_states).max(1)[0].detach()
                target_q = rewards + gamma * next_q * (1 - dones)
                loss = nn.MSELoss()(current_q.squeeze(), target_q)

            optimizer.zero_grad()
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        save_every = 1000
        print_every = 1000
        if episode % print_every == 999:
            avg_score = sum(scores[-print_every:]) / print_every
            avg_reward = sum(total_rewards[-print_every:]) / print_every
            print(f'Episode: {episode + 1}, Avg Score: (last {print_every}): {avg_score:.2f}, Avg Total Reward: (last {print_every}): {avg_reward:.2f}, Epsilon: {epsilon:.2f}')

        if (episode + 1) % save_every == 0:
            save_model(model, f'snake_model_{episode + 1}.pth')

    save_model(model, 'final_snake_model.pth')
    print('Final model saved')

if __name__ == '__main__':
    train()