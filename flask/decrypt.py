from cryptography.fernet import Fernet
import pickle

class DECRYPT():

    def initialize_variables(self, key, encrypted_data):
        self.key = key
        # self.path = path
        self.encrypted_data = encrypted_data

        self.decrypted_value = ''

    def decrypt_data(self, encrypted_data, key):
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        return decrypted_data

    # def read_from_temp_folder(self, temp_file_path):
    #     with open(temp_file_path, 'rb') as temp_file:
    #         data = temp_file.read()
    #     return data

    def get_decrypted(self):
        return self.decrypted_value

    def __init__(self, key, encrypted_data):
        
        self.initialize_variables(key, encrypted_data)

        # self.encrypted_data = self.read_from_temp_folder(self.path)

        self.decrypted_value = self.decrypt_data(self.encrypted_data, self.key)

        self.decrypted_value = pickle.loads(self.decrypted_value)


        

