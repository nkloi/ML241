import numpy as np
import csv

# Softmax function
def softmax_function(Z):
    exp_Z = np.exp(Z - np.max(Z, axis=0, keepdims=True))
    return exp_Z / np.sum(exp_Z, axis=0, keepdims=True)

# Read Weight and Bias from csv 
def load_weights_and_bias(filename='weight.csv'):
    W = []
    B = []

    # Read file CSV
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        header = next(reader)
        for row in reader:
            if row[0] == 'Bias':
                break
            W.append([float(value) for value in row])

        for row in reader:
            if row:  
                B.append(float(row[0]))

    W = np.array(W)
    B = np.array(B).reshape(-1, 1)

    return W, B

# Predict function
def predict_quality(X, W, B):
    Z = np.dot(W, X.T) + B 
    return softmax_function(Z)

W_loaded, B_loaded = load_weights_and_bias('weight.csv')

print("W và B đã được đọc từ 'weight.csv'.")

# Standardize input function based on custom binning logic
def custom_standardize_input(N, P, K):
    # Standardize N
    if 60 <= N <= 90:
        N_standardized = 1
    elif 90 < N <= 120:
        N_standardized = 2
    elif 120 < N <= 150:
        N_standardized = 3
    elif N > 150:
        N_standardized = 4
    else:
        N_standardized = 0

    # Standardize P
    if 5 <= P <= 10:
        P_standardized = 1
    elif 10 < P <= 20:
        P_standardized = 2
    elif 20 < P <= 40:
        P_standardized = 3
    elif P > 40:
        P_standardized = 4
    else:
        P_standardized = 0

    # Standardize K
    if 50 <= K <= 100:
        K_standardized = 1
    elif 100 < K <= 150:
        K_standardized = 2
    elif 150 < K <= 200:
        K_standardized = 3
    elif K > 200:
        K_standardized = 4
    else:
        K_standardized = 0

    return np.array([N_standardized, P_standardized, K_standardized])

# Function to read CSV file and make predictions
def evaluate_accuracy_from_csv(input_filename='input_data.csv'):
    correct_predictions = 0
    total_predictions = 0

    with open(input_filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            N = float(row['Đạm (N) mg/kg'])
            P = float(row['Lân (P) mg/kg'])
            K = float(row['Kali (K) mg/kg'])
            true_class = row['Thang đánh giá']

            # Standardize input
            input_values = custom_standardize_input(N, P, K)

            # Make prediction
            Y_pred = predict_quality(input_values.reshape(1, -1), W_loaded, B_loaded)

            # The class with the highest probability
            predicted_class = np.argmax(Y_pred)

            # Convert true class to numeric label
            if true_class == 'Thấp, nghèo':
                true_class_label = 0
            elif true_class == 'Trung bình':
                true_class_label = 1
            elif true_class == 'Trung bình đến giàu':
                true_class_label = 2
            elif true_class == 'Rất giàu':
                true_class_label = 3

            # Compare predictions with true class and calculate accuracy
            if predicted_class == true_class_label:
                correct_predictions += 1
            total_predictions += 1

            print(f"\nDự đoán cho dòng {row['STT']}:")
            print(f"  Giá trị thực tế: {true_class}")
            print(f"  Dự đoán: {['Thấp, nghèo', 'Trung bình', 'Trung bình đến giàu', 'Rất giàu'][predicted_class]}")

    # Calculate accuracy
    accuracy = correct_predictions / total_predictions * 100
    print(f"\nAccuracy: {accuracy:.2f}%")

# Call the function to evaluate the model using data from a CSV file
evaluate_accuracy_from_csv('dataset_bonus.csv')



# Function to get input from the user and make a prediction
def get_input_and_predict():
    N = float(input("Nhập giá trị Nitrogen (N) (mg/kg): "))
    P = float(input("Nhập giá trị Phosphorus (P) (mg/kg): "))
    K = float(input("Nhập giá trị Potassium (K) (mg/kg): "))
    
    # Use custom normalization function
    input_values = custom_standardize_input(N, P, K)

    Y_pred = predict_quality(input_values.reshape(1, -1), W_loaded, B_loaded)
    
    print("\nXác suất dự đoán cho từng lớp chất lượng:")
    print(Y_pred)
    
    # The class with the highest probability
    predicted_class = np.argmax(Y_pred)
    print(f"Lớp dự đoán: {predicted_class}")

    if predicted_class == 0:
        print("Lớp dự đoán: Đất thấp, nghèo")
    elif predicted_class == 1:
        print("Lớp dự đoán: Đất trung bình")
    elif predicted_class == 2:
        print("Lớp dự đoán: Đất trung bình, giàu")
    elif predicted_class == 3:
        print("Lớp dự đoán: Đất rất giàu")
    else:
        print("Lớp dự đoán: Không xác định")

# Call the function to allow the user to input data and make a prediction
get_input_and_predict()