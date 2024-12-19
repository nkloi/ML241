import pickle
import traceback
import tensorflow as tf
from fastapi import FastAPI, Response
from pydantic import BaseModel
from utils.data_preprocessing import clean_text
from tensorflow.keras import models # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore

app = FastAPI()

model = models.load_model('models/best_model.h5')

class PredictionInput(BaseModel):
    comment: str

@app.get('/')
async def welcome():
    return {'message': 'Welcome!'}

@app.post('/predict')
async def predict(input_data: PredictionInput, response: Response):
    try:      
        max_len = 50
        with open('./models/tokenizer.pkl', "rb") as f:
            tokenizer = pickle.load(f)
        comment = clean_text(input_data.comment)
        sequence = tokenizer.texts_to_sequences([comment])
        padded_sequence = pad_sequences(sequence, maxlen=max_len)
        pred_prob = model.predict(padded_sequence)
        pred = tf.argmax(pred_prob, axis=1).numpy()
        pred = pred[0]
        if pred == 0:
            return {
                'sentiment': 'Negative',
                'message': 'Sucessfully!'
            }
        elif pred == 1:
            return {
                'sentiment': 'Neutral',
                'message': 'Sucessfully!'
            }
        elif pred == 2:
            return {
                'sentiment': 'Positive',
                'message': 'Sucessfully!'
            }

    except Exception as e:
        response.status_code = 500
        return {
            'sentiment': 'Unknown',
            'message': f'An unexpected error occurred: {traceback.format_exc()}'
        }