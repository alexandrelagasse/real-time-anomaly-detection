import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
from joblib import load
from sklearn.metrics import roc_curve, precision_recall_curve, auc, f1_score
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/cleaned_creditcard.csv")
X = df.drop(columns=["Class"])
y = df["Class"]

# Load scaler and model
scaler = load("models/scaler.pkl")
autoencoder = load_model("models/autoencoder_model.keras")

# Scale features
X_scaled = scaler.transform(X)

# Get reconstruction errors
X_pred = autoencoder.predict(X_scaled)
mse = np.mean(np.power(X_scaled - X_pred, 2), axis=1)

# Compute ROC curve and AUC
fpr, tpr, roc_thresholds = roc_curve(y, mse)
roc_auc = auc(fpr, tpr)

# Compute Precision-Recall curve and AUC
precision, recall, pr_thresholds = precision_recall_curve(y, mse)
pr_auc = auc(recall, precision)

# Find optimal threshold for F1 (maximizes f1 score)
f1_scores = [(f1_score(y, mse > thresh), thresh) for thresh in pr_thresholds]
best_f1, best_thresh = max(f1_scores, key=lambda x: x[0])

# Plot ROC curve
plt.figure()
plt.plot(fpr, tpr)
plt.title(f"ROC Curve (AUC = {roc_auc:.3f})")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.grid(True)
plt.show()

# Plot Precision-Recall curve
plt.figure()
plt.plot(recall, precision)
plt.title(f"Precision-Recall Curve (AUC = {pr_auc:.3f})")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.grid(True)
plt.show()

print(f"Optimal threshold for max F1 ({best_f1:.3f}): {best_thresh:.5f}")
