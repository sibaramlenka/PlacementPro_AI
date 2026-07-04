import pandas as pd
import pickle

model = pickle.load(open("models/placement_model.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

columns = [
    "CGPA",
    "Internships",
    "Projects",
    "Workshops/Certifications",
    "AptitudeTestScore",
    "SoftSkillsRating",
    "PlacementTraining"
]

def predict(data):
    df = pd.DataFrame([data], columns=columns)
    scaled = scaler.transform(df)

    prob = model.predict_proba(scaled)[0][1]

    print("\nProbability of Placement:", round(prob, 2))

    if prob >= 0.7:
        print(" High Chance of Placement")
    elif prob >= 0.4:
        print(" Medium Risk / Uncertain")
    else:
        print(" High Risk (Not Likely Placed)")

# TEST CASES
predict([4,0,1,0,40,50,0])
predict([7,1,3,2,70,65,1])
predict([9,1,4,3,90,90,1])