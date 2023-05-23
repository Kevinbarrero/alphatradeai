
import numpy as np
import pandas as pd
import os
from fastapi import FastAPI

import indicators as ind
import db_connect as db
import pandas_ta as pta
from fastapi.middleware.cors import CORSMiddleware
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with the appropriate list of allowed origins
    allow_methods=["*"],  # Replace "*" with the appropriate list of allowed HTTP methods
    allow_headers=["*"],  # Replace "*" with the appropriate list of allowed HTTP headers
)

@app.get("/model/{model_name}")
async def read_item(model_name: str):
    data = db.get_db_data(model_name)
    rsi6 = pta.rsi(data["close"], length=6)
    data = data.assign(Rsi6=rsi6)
    data = data.drop({'open_time', 'close_time', 'n_trades', 'volume'}, axis=1)
    data = data.dropna()
    scaler = MinMaxScaler(feature_range=(0, 1))
    data['close'] = scaler.fit_transform(data['close'].values.reshape(-1, 1))
    data['open'] = scaler.fit_transform(data['open'].values.reshape(-1, 1))
    data['high'] = scaler.fit_transform(data['high'].values.reshape(-1, 1))
    data['low'] = scaler.fit_transform(data['low'].values.reshape(-1, 1))

    model = load_model('neural_model2.h5')
    next_10_predictions = scaler.inverse_transform(model.predict(np.array([data[-60:]])))
    
    return {"pred": next_10_predictions.reshape(-1).tolist()}
