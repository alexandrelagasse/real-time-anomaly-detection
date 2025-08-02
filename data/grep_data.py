import pandas as pd
import os
import kagglehub
import shutil

local_path = os.path.join(os.path.dirname(__file__), "creditcard.csv")

if os.path.exists(local_path):
    print("Fichier creditcard.csv trouvé localement!")
    path = local_path
else:
    print("Fichier creditcard.csv non trouvé localement. Téléchargement depuis Kaggle...")
    kaggle_path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
    kaggle_file = os.path.join(kaggle_path, "creditcard.csv")
    
    shutil.copy2(kaggle_file, local_path)
    print(f"Fichier copié vers: {local_path}")
    path = local_path

try:
    df = pd.read_csv(path)
    print("Fichier creditcard.csv importé avec succès!")
    print(f"Dimensions du dataset: {df.shape}")
    print(f"Colonnes: {list(df.columns)}")
    print(f"Premières lignes:")
    print(df.head())
except FileNotFoundError:
    print(f"Erreur: Impossible de trouver le fichier creditcard.csv")
    print(f"Chemin essayé: {path}")
except Exception as e:
    print(f"Erreur lors de l'import: {e}")