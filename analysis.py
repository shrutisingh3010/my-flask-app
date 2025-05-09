import pandas as pd
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

tknizer = Tokenizer()


df = pd.read_csv(r'preprocessed_dataset.csv')
model = keras.models.load_model(r'best.h5')

df.dropna(inplace=True)
tknizer.fit_on_texts(df.Clean)

def score_to_sentiment(score, include_neutral=True):
  if include_neutral:
        label = 'Neutral'
        if score <= 0.42:
            label = 'Negative'
        elif score >= 0.58:
            label = 'Positive'
        return label
  else:
      return 'Negative' if score < 0.5 else 'Positive'

def predict(text, include_neutral=True):
    # Tokenize text
    x_test = pad_sequences(tknizer.texts_to_sequences([text]), maxlen=140)
    # Predict
    score = model.predict([x_test])[0]
    # Decode sentiment
    label = score_to_sentiment(score, include_neutral)

    return {"text": text, "label": label, "score": float(score)}