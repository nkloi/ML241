import numpy as np
import csv
from sklearn.preprocessing import StandardScaler

# Read data from CSV file
with open('dataset.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    # Skip the first row (header)
    next(reader)
    
    # Create lists to hold values from the columns
    column_2 = []
    column_3 = []
    column_4 = []
    column_5 = [] 

    # Read and add data to the lists
    for row in reader:
        column_2.append(int(row[1]))
        column_3.append(int(row[2]))
        column_4.append(int(row[3]))
        column_5.append(row[4])       

# Convert data into numpy arrays
N = np.array(column_2)
P = np.array(column_3)
K = np.array(column_4)
QC = np.array(column_5)

# Encode the rating scale into numerical values
labels = {'Thấp, nghèo': 0, 'Trung bình': 1, 'Trung bình đến giàu': 2, 'Rất giàu': 3}
Y = np.array([labels[qc] for qc in QC])

# Convert Y to one-hot encoding
m = Y.shape[0]
Y_one_hot = np.zeros((m, 4))
Y_one_hot[np.arange(m), Y] = 1

# Function to convert N, P, K according to the given ranges
def custom_standardize(N, P, K):
    # Convert N
    N_standardized = np.digitize(N, bins=[60, 90, 120, 150], right=False)
    # Convert P
    P_standardized = np.digitize(P, bins=[5, 10, 20, 40], right=False)
    # Convert K
    K_standardized = np.digitize(K, bins=[50, 100, 150, 200], right=False)
    return N_standardized, P_standardized, K_standardized

# Apply custom convert value
N_standardized, P_standardized, K_standardized = custom_standardize(N, P, K)

# Combine features into the matrix X
X = np.column_stack((N_standardized, P_standardized, K_standardized))

# Create weight matrix W
W = np.random.randn(4, 3)

# Create vector bias B
B = np.random.randn(4, 1)

# Softmax function
def softmax_function(Z):
    exp_Z = np.exp(Z - np.max(Z, axis=0, keepdims=True))
    return exp_Z / np.sum(exp_Z, axis=0, keepdims=True)

# Predict function
def predict(X, B, W):
    Z = np.dot(W, X.T) + B
    return softmax_function(Z)

# Cost function
def cross_entropy_loss(X, Y, B, W):
    m = len(Y)
    epsilon = 1e-15
    Y_pred = predict(X, B, W) 
    cost = - np.sum(Y.T * np.log(Y_pred + epsilon)) / m  
    return cost

# Compute gradients for W and B
def compute_gradients(X, Y, Y_pred):
    m = X.shape[0]
    dZ = Y_pred - Y.T
    dW = np.dot(dZ, X) / m
    dB = np.sum(dZ, axis=1, keepdims=True) / m
    return dW, dB

# Mini-Batch Gradient Descent
def mini_batch_gradient_descent(X, Y, W, B, learning_rate, num_iterations, batch_size):
    m = X.shape[0]
    for i in range(num_iterations):
        # Shuffle data to ensure randomness in each batch
        indices = np.random.permutation(m)
        X_shuffled = X[indices]
        Y_shuffled = Y[indices]
        
        # Divide to mini-batches
        for j in range(0, m, batch_size):
            X_batch = X_shuffled[j:j+batch_size]
            Y_batch = Y_shuffled[j:j+batch_size]
            
            # Compute predict and cost
            Y_pred = predict(X_batch, B, W)
            loss = cross_entropy_loss(X_batch, Y_batch, B, W)
            
            # Compute gradient
            dW, dB = compute_gradients(X_batch, Y_batch, Y_pred)
            
            # Update W and B
            W -= learning_rate * dW
            B -= learning_rate * dB
        
        print(f"Iteration {i}: Loss = {loss}")
        
    return W, B

# Save weight and bias to csv file Fuction
def save_weights_and_bias(W, B, filename='weight.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerow(['W1', 'W2', 'W3'])
        for row in W:
            writer.writerow(row)
        
        writer.writerow(['Bias'])
        for b in B:
            writer.writerow([b[0]])

# Hyperparameters
learning_rate = 0.01
num_iterations = 1000
batch_size = 32

# Training the model
W, B = mini_batch_gradient_descent(X, Y_one_hot, W, B, learning_rate, num_iterations, batch_size)

# Print final weight matrix W and B
print("\nFinal Weight Matrix W:")
print(W)
print("\nFinal Bias Matrix B:")
print(B)

# Save final weight matrix W and B
save_weights_and_bias(W, B)
print("W và B đã được lưu vào 'weight.csv'.")