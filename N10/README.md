# ML241 - Snake Game AI using Deep Q-Learning
# Snake Game AI using Deep Q-Learning

## Overview
Dự án này là một triển khai của thuật toán Deep Q-Learning để huấn luyện AI chơi trò chơi Snake. AI sẽ học cách điều khiển con rắn để tìm và ăn mồi, đồng thời tránh va chạm với tường và thân rắn.

## Demo
![Example screenshot](./img/demo.gif)

## Features
- AI tự học chơi Snake thông qua Deep Q-Learning
- Visualization của quá trình chơi game bằng Pygame
- Khả năng lưu và tải các model đã train
- Real-time rendering của game với điểm số
- Tự động load checkpoint mới nhất khi test

## Technologies and Tools
- Python 3.9
- PyTorch - Framework deep learning
- Pygame - Visualization game
- Các thư viện Python khác:
  - numpy
  - collections (deque)
  - random
  - os
  - time

## Technical Details
### Neural Network Architecture
- Input layer: 26 neurons (game state features)
- Hidden layers: 
  - FC1: 64 neurons
  - FC2: 128 neurons
  - FC3: 64 neurons
- Output layer: 4 neurons (các hướng di chuyển có thể)

### Training Parameters
- Batch size: 16384
- Learning rate: 0.0001
- Gamma (discount factor): 0.99
- Epsilon decay: 0.9997
- Minimum epsilon: 0.01
- Memory size: 100000
- Optimizer: Adam

## Setup and Installation

### Yêu cầu hệ thống
- Python 3.9 trở lên
- Conda (khuyến nghị) hoặc Python virtual environment
- GPU (không bắt buộc, nhưng sẽ giúp tăng tốc quá trình training)

### Cài đặt môi trường

1. Clone repository:
git clone [URL của repository]
cd [tên thư mục project]
2. Tạo môi trường ảo với Conda:
conda create -n snake_env python=3.9
3. Kích hoạt môi trường:
conda activate snake_env

Cài đặt các dependencies: python -m pip install -r requirements.txt
Usage
Training
Để bắt đầu training model: python train.py
Testing
Để xem AI chơi game: python test.py
Contact
Email: huy.nguyenminh108@hcmut.edu.vn
---------------------------------------------------
Cách khác có thể chạy trực tiếp trên môi trường google colab không cần cài đặt nhiều 
1 Copy 3 file train, test, .pth lên google colab (khác là phải thay file test.py khác so với khi chạy trên máy của mình)