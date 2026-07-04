import pickle
from train_model import model,scaler
with open("models/placement_model.pkl","wb") as file:
    pickle.dump(model,file)
with open("models/scaler.pkl","wb") as file:
    pickle.dump(scaler,file)
print("Model saved successfully")