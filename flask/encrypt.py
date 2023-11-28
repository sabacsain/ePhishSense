from cryptography.fernet import Fernet
import tempfile
import os, pickle

class ENCRYPT():

    def initialize_variables(self, mail_object, email, password):
        self.mail_object = mail_object
        self.email = email
        self.password = password
        # self.temp_path = ''
        self.key = ''
        self.connection_info = {}
        self.serialized_data = ''

        self.encrypted_value = ''

    def encrypt_data(self, data, key):
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(data)
        return encrypted_data

    def store_connection(self):
        self.connection_info = {
        'server': 'imap.gmail.com',
        'port': self.mail_object.port,
        'email': self.email,
        'password': self.password
        }

    # def write_to_temp_folder(self, data):
    #     temp_dir = tempfile.gettempdir()
    #     temp_file_path = os.path.join(temp_dir, "encrypted_data.txt")

    #     with open(temp_file_path, 'wb') as temp_file:
    #         temp_file.write(data)

    #     return temp_file_path

    def get_encrypted(self):
        return self.encrypted_value

    def get_key(self):
        return self.key

    def get_path(self):
        return self.temp_path

    def __init__(self, mail_object, email, password):


        self.initialize_variables(mail_object, email, password)
 
        self.store_connection()
  
        self.serialized_data = pickle.dumps(self.connection_info)

        # Replace 'your_secret_key' with a securely generated key.
        self.key = Fernet.generate_key()

        # Encrypt the string
        self.encrypted_value = self.encrypt_data(self.serialized_data, self.key)

        # Write the encrypted data to the temporary folder
        # self.temp_path = self.write_to_temp_folder(self.encrypted_value)

        # print(f"ENCRYPTED PATH: {self.temp_path}")


