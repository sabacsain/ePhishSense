import pickle, os, platform

class DT_MODEL():
    
    def __init__(self, input):
        self.loaded_model = None
        self.input = input
        self.get_filepath()
        self.loadModel()
        self.label = self.predict()


    def result(self):

        return self.label

    # Get DT Model Filepath
    def get_filepath(self):
        # Get the OS 
        which_os = platform.system()

        # Perform forward/backward slash depending on the OS
        slash = '\\' if which_os == 'Windows' else '/'

        # Get the current directory
        current_path = os.path.dirname(os.path.abspath(__file__))

        # Concatenate directory path and dataset location
        filepath = current_path + slash + 'dt_model.pkl'

        return filepath

    # Load the model from the file
    def loadModel(self):
        with open(self.get_filepath(), 'rb') as model_file:
            self.loaded_model = pickle.load(model_file)

    # Predict new input email
    def predict(self):
        predicted_label = self.loaded_model.predict([self.input])
        if predicted_label == 0:
            return 'Safe'
        elif predicted_label == 1:
            return 'Malicious'
        else: 
            return 'System Error!'



