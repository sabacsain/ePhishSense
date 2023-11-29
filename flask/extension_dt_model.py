import pickle, os, platform, joblib

class DT_MODEL():
    
    def __init__(self, input):
        self.loaded_model = None
        self.input = input
        self.filepath = self.get_filepath()
        self.loaded_model = self.loadModel()
        self.label = self.predict()


    def result(self):
        return self.label

    # Get DT Model Filepath
    def get_filepath(self):
        print("start FILEPATH")
        # Get the OS 
        which_os = platform.system()

        # Perform forward/backward slash depending on the OS
        slash = '\\' if which_os == 'Windows' else '/'

        # Get the current directory
        current_path = os.path.dirname(os.path.abspath(__file__))

        # Concatenate directory path and dataset location
        filepath = current_path + slash + 'dt_model.pkl'

        print("end FILEPATH")

        return filepath

    # Load the model from the file
    def loadModel(self):
        print("start LOAD MODEL")
        with open(self.filepath, 'rb') as model_file:
            model = joblib.load(model_file)
        print("end LOAD MODEL")
        return model

    # Predict new input email
    def predict(self):
        print("start PREDICT")
        predicted_label = self.loaded_model.predict([self.input])
        print("end PREDICT")
        if predicted_label == 0:
            return 'Safe'
        elif predicted_label == 1:
            return 'Malicious'
        else: 
            return 'System Error!'




