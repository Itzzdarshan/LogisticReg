import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

# 1. Load the tactical 8-column dataset
df = pd.read_csv("pubg_pro_terminal.csv")

# 2. Define our 8 Features (X) and Target (y)
features = ['Kills', 'Damage', 'Boosts', 'Heals', 'Distance', 'Weapons', 'Revives', 'Headshots']
X = df[features]
y = df['is_pro']

# 3. Apply Scaling (Mandatory for Logistic Regression with different units)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Train the Logistic Regression Model
model = LogisticRegression()
model.fit(X_scaled, y)

# 5. Save the Brain (model) and the Translator (scaler)
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ MISSION ACCOMPLISHED: model.pkl and scaler.pkl created for 8 features!")