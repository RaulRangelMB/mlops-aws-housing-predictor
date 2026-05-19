import joblib
import pandas as pd

FEATURE_NAMES = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup", "Latitude", "Longitude"]

class HousingPredictor:
    def __init__(self):
        # load model
        self.model = joblib.load("model.joblib")

    def predict_price(self, features):
        """Formats features and calls the scikit-learn regressor model."""

        prediction_input = [features] if not isinstance(features[0], list) else features

        df_input = pd.DataFrame(prediction_input, columns=FEATURE_NAMES)
        raw_prediction = self.model.predict(df_input)[0]
        
        return {
            "raw_value": float(raw_prediction),
            "usd_price": float(raw_prediction * 100000)
        }