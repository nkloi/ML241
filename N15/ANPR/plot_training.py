import matplotlib.pyplot as plt

def plot_training_results(num_chars_detected, training_times):
    """
    Vẽ biểu đồ huấn luyện:
    - Biểu đồ số lượng ký tự nhận diện được qua từng ảnh.
    - Biểu đồ thời gian huấn luyện cho từng ảnh.
    """

    # Biểu đồ số ký tự nhận diện được
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(num_chars_detected, label='Number of Characters Detected', marker='o')
    plt.title('Number of Characters Detected in Each Image')
    plt.xlabel('Image Index')
    plt.ylabel('Number of Characters')
    plt.grid(True)
    plt.legend()

    # Biểu đồ thời gian huấn luyện
    plt.subplot(1, 2, 2)
    plt.plot(training_times, label='Training Time (seconds)', marker='x', color='r')
    plt.title('Training Time per Image')
    plt.xlabel('Image Index')
    plt.ylabel('Training Time (seconds)')
    plt.grid(True)
    plt.legend()

    # Hiển thị các biểu đồ
    plt.tight_layout()
    plt.show()
