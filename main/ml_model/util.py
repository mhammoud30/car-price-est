import pickle
import json
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

__car_models = None
__data_columns = None
__model = None


def get_estimated_price(model,year,transmission,condition,odometer):
    try:
        loc_index = __data_columns.index(model.lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = year
    x[1] = transmission
    x[2] = condition
    x[3] = odometer
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)


def get_carModel_names():
    return __car_models


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __car_models

    with open(BASE_DIR / "ml_model/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __car_models = __data_columns[4:]  # first 4 columns are "year", "transmission", "condition", "odometer"

    global __model
    if __model is None:
        with open(BASE_DIR / "ml_model/used_car_price_model.pickle" , "rb") as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")


def get_data_columns():
    return __data_columns


if __name__ == '__main__':
    load_saved_artifacts()