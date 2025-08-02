#!/usr/bin/env python3

try:
    import numpy
    print(f"✅ numpy détecté, version = {numpy.__version__}")
    
    import sklearn
    print(f"✅ scikit-learn détecté")
    
    import joblib
    print(f"✅ joblib détecté")
    
    print("✅ Toutes les dépendances sont installées correctement!")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}") 