import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras import regularizers
from joblib import dump
import os

df = pd.read_csv("data/cleaned_creditcard.csv")

X = df.drop(columns=["Class"])
y = df["Class"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

iso_model = IsolationForest(contamination=0.001, random_state=42)
iso_model.fit(X_train[y_train == 0])  # only normal data

# Predict (1 = fraud, 0 = normal)
iso_preds = iso_model.predict(X_test)
iso_preds = np.where(iso_preds == -1, 1, 0)

print("📌 Isolation Forest Results :")
print(classification_report(y_test, iso_preds))

input_dim = X_train.shape[1]
input_layer = Input(shape=(input_dim,))
encoder = Dense(14, activation="relu", activity_regularizer=regularizers.l1(1e-5))(input_layer)
encoder = Dense(7, activation="relu")(encoder)
decoder = Dense(14, activation='relu')(encoder)
decoder = Dense(input_dim, activation='linear')(decoder)
autoencoder = Model(inputs=input_layer, outputs=decoder)

autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.fit(
    X_train[y_train == 0], X_train[y_train == 0],
    epochs=10, batch_size=256, shuffle=True, validation_split=0.1, verbose=1
)

X_test_pred = autoencoder.predict(X_test)
mse = np.mean(np.power(X_test - X_test_pred, 2), axis=1)

threshold = np.percentile(mse[y_test == 0], 95)
ae_preds = (mse > threshold).astype(int)

print("📌 AutoEncoder Results :")
print(classification_report(y_test, ae_preds))

os.makedirs("models", exist_ok=True)
dump(iso_model, "models/isolation_forest.pkl")
autoencoder.save("models/autoencoder_model.keras")
dump(scaler, "models/scaler.pkl")
