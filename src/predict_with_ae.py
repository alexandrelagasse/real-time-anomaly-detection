import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
from joblib import load


scaler = load("models/scaler.pkl")
autoencoder = load_model("models/autoencoder_model.keras")

df = pd.read_csv("data/cleaned_creditcard.csv")
X = df.drop(columns=["Class"])
y = df["Class"]

X_scaled = scaler.transform(X)

X_pred = autoencoder.predict(X_scaled)
mse = np.mean(np.power(X_scaled - X_pred, 2), axis=1)


threshold = np.percentile(mse[y == 0], 99)
preds = (mse > threshold).astype(int)

print("Nombre de fraudes détectées :", preds.sum())
print("Nombre de vraies fraudes    :", y.sum())

df_results = df.copy()
df_results["prediction"] = preds
df_results["actual"] = y
print(df_results.head(20))

