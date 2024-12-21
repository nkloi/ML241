# Sentiment Analysis of Product Reviews

## About The Project

Sentiment Analysis plays a crucial role in understanding customer opinions and improving products or services. In this project, we focus on analyzing sentiments from Vietnamese product reviews using a Bidirectional LSTM model. The dataset utilized is the **Vietnamese Sentiment Analysis**, which can be accessed [here](https://www.kaggle.com/datasets/linhlpv/vietnamese-sentiment-analyst/data).

The primary goal of this project is to build an API that accurately determines the sentiment of a given review, classifying it as positive, negative or neutral.

### Built With

- Python
- Tensorflow
- FastAPI

## Getting Started

To start the project, you need to install the necessary software and follow the steps below.

### Prerequisites

- Google Colab (recommended) or any platform that supports running Jupyter Notebooks and provides GPU acceleration, such as Kaggle, AWS SageMaker, or Azure Machine Learning, can significantly speed up the training process for your model.
- Anaconda (recommended) or a Python virtual environment is used to create an isolated environment for installing the dependencies required to run the API built from your model.

### Training

1. Open Jupyter Notebook

   Open `notebooks\sentiment_analysis.ipynb` in Google Colab or any other platform that supports running Jupyter Notebooks.

2. Run Jupyter Notebook

   In this Jupyter Notebook, we use data from the `data` directory and a function from the `utils` directory, so we connect to both Google Drive and GitHub to access them. You can upload the entire project folder to your Google Drive, connect to your Drive and change directory to the corresponding paths. After that, you can run Jupyter Notebook to train a new model.

### Running the Application

1. Setup Python environment

   Set up Python environment using Anaconda or Python virtual environment.

   If you are using a pre-trained model from the models directory, you should use Python version 3.10.12. However, if you have retrained the model, make sure to use the same Python version as the one used in the environment where the model was trained to avoid errors when loading the model.

2. Install dependencies

   If you have retrained a new model, make sure to adjust the TensorFlow version in the `requirements.txt` file to match the version of TensorFlow used during training.

   Make sure you are in the `Sentiment Analysis` directory in a terminal.

   ```sh
   pip install -r requirements.txt
   ```

3. Start FastAPI Application

   ```sh
   uvicorn app:app --reload
   ```

   Open docs page and test API at [http://localhost:8000/docs](http://localhost:8000/docs)
