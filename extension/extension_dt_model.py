import pickle

class DT_MODEL():
    
    # Load the model from the file
    def loadModel(self):
        with open('dt_model.pkl', 'rb') as model_file:
            self.loaded_model = pickle.load(model_file)

    # Predict new input email
    def predict(self, input):
        self.input = input
        predicted_label = self.loaded_model.predict([self.input])
        if predicted_label == 0:
            return 'Safe'
        elif predicted_label == 1:
            return 'Malicious'
        else: 
            return 'System Error!'

    def __init__(self, input):
        self.loadModel()
        self.predict(input)


