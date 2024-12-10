import gradio as gr
from torch import nn
import torch

class MLPModel(nn.Module):
    def __init__(self, input_dim, num_classes, hidden_dims=[128, 64], dropout=0):
        """
        Args:
            input_dim (int): Số lượng đặc trưng đầu vào (input features).
            num_classes (int): Số lớp (outputs).
            hidden_dims (list): Danh sách số lượng neurons ở mỗi layer ẩn.
            dropout (float): Tỷ lệ dropout để tránh overfitting.
        """
        super(MLPModel, self).__init__()
        
        layers = []
        in_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(in_dim, hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            in_dim = hidden_dim
        
        layers.append(nn.Linear(in_dim, num_classes))
        
        self.mlp = nn.Sequential(*layers)
        self.softmax = nn.Softmax(-1)
    def forward(self, x):
        output = self.mlp(x)
        output = self.softmax(output)
        return output
    
# Initialize the dummy model (replace with your trained model)
model = MLPModel(36,3)

# Load your model here (if already trained):
model_path = f"./MLP_model.pth"
model.load_state_dict(torch.load(model_path, weights_only=True))
model.eval()

def process_file(file):
    
    # Read the contents of the file
    #contents = file.read().decode("utf-8")
    try:
        # If the input is a file-like object, read its contents
        if hasattr(file, "read"):
            contents = file.read().decode("utf-8")

        # If the input is a string (file path), read it directly
        elif isinstance(file, str):
            with open(file, "r", encoding="utf-8") as f:
                contents = f.read()
        else:
            return "Error: Unsupported file input type."
    except Exception as e:
        return f"Error: Could not read the file. Details: {e}"
    
    # Split the contents by lines
    lines = contents.splitlines()

    # Ensure we have exactly 36 features
    if len(lines) != 36:
        return "Error: The file should contain exactly 36 lines of data."
    
    # Extract values as a list (assuming the format "Feature x value")
    features = [float(line.split()[1]) for line in lines]  # Convert to float for model input
    
    # Convert to numpy array or torch tensor for the model (assuming torch model)
    input_data = torch.tensor(features, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
    # Get model prediction
    with torch.no_grad():
        prediction = model(input_data)

    # Convert to list for multi-element outputs
    prediction_list = prediction.numpy().tolist()

    #  # Convert to list for multi-element outputs
    # prediction_list = prediction.numpy().tolist()[0]

    # Map the index of the highest value to a label
    labels = {0: "Enroll", 1: "Dropout", 2: "Graduate"}
    predicted_class = labels[int(torch.argmax(prediction))]
    
    return f"Model Prediction: {predicted_class}"

# Gradio Interface for File Upload and Model Prediction
iface = gr.Interface(
    fn=process_file,  # The function to process the input file and get prediction
    inputs=gr.File(label="Upload a TXT File with 36 Features"),  # Input for the txt file
    outputs="text",  # Output the prediction as text
    title="36 Features Model Predictor",  # Title of the interface
    description="Upload a .txt file containing exactly 36 lines, each representing a feature.",  # Description
)

# Launch the interface
iface.launch()