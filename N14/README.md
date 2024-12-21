## Setup

1. Create and activate Virtual Environment:

    ```sh
    python -m venv .venv
    ```
    On Windows
    ```sh
    .\.venv\Scripts\activate
    ```
    On macOS/Linux
    ```sh
    source .venv/bin/activate
    ```

2. Install the required libraries:

    ```sh
    pip install -r requirements.txt
    ```

3. Run the Jupyter notebook:

    ```sh
    jupyter notebook main.ipynb
    ```

## Usage

- **Data Preprocessing**: Preprocess the movie, ratings, and tags data.
- **Model Training**: Train collaborative filtering models using the Surprise library.
- **Recommendations**: Generate movie recommendations for users.

## Data Visualization

The Jupyter notebook includes data visualization steps to help understand the data distribution and model performance.

## License

This project is licensed under the MIT License.