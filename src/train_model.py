print("Training Placement Risk AI...")

import pandas as pd
import numpy as np

data = pd.read_csv("data/placementdata.csv")

if "StudentID" in data.columns:
    data.drop("StudentID", axis=1, inplace=True)

# Clean target
data["PlacementStatus"] = data["PlacementStatus"].str.strip().str.lower()
data["PlacementStatus"] = data["PlacementStatus"].map({"placed": 1, "notplaced": 0})

# Clean categorical
data["PlacementTraining"] = data["PlacementTraining"].str.strip().str.lower()
data["PlacementTraining"] = data["PlacementTraining"].map({"yes": 1, "no": 0})

X = data.drop(["PlacementStatus", "ExtracurricularActivities", "SSC_Marks", "HSC_Marks"], axis=1)
y = data["PlacementStatus"]

print("Class distribution:")
print(y.value_counts())

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)

X_train, y_train = smote.fit_resample(X_train, y_train)

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=400,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

from sklearn.metrics import accuracy_score

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
import pickle

pickle.dump(model, open("models/placement_model.pkl", "wb"))
pickle.dump(scaler, open("models/scaler.pkl", "wb"))

print("Model saved successfully!")

feature_names = X.columns

for feature, importance in zip(feature_names, model.feature_importances_):
    print(f"{feature}: {importance:.3f}")

