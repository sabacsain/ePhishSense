from cryptography.fernet import Fernet
import imaplib
import pickle

class IMAP_CIPHER():

    def initialize_variables(self, ):
        self.plain_text = str(plain_text)
        self.temp_path = ''
        self.key = ''

        self.encrypted_value = ''


    # Function to encrypt data
    def encrypt_data(data, key):
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(data)
        return encrypted_data

    # Function to decrypt data
    def decrypt_data(encrypted_data, key):
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        return decrypted_data

    # Assume 'imap_connection' is your IMAP4_SSL object
    imap_connection = imaplib.IMAP4_SSL('your_mail_server.com')

    # Extract relevant information
    connection_info = {
        'server': 'imap.google.com',
        'port': imap_connection.port,
        'username': email,
        'password': password,  # Note: Securely store and manage passwords
    }

    # Serialize the connection information to a string
    serialized_data = pickle.dumps(connection_info)

    # Replace 'your_encryption_key' with a securely generated key.
    encryption_key = Fernet.generate_key()

    # Encrypt the serialized data
    encrypted_data = encrypt_data(serialized_data, encryption_key)

    # You can save the encrypted data to a file or send it over the network, for example.

    # Decrypt the data back to the connection information
    decrypted_data = decrypt_data(encrypted_data, encryption_key)
    deserialized_info = pickle.loads(decrypted_data)

    # Recreate the IMAP connection using the stored information
    new_imap_connection = imaplib.IMAP4_SSL(deserialized_info['server'], deserialized_info['port'])
    new_imap_connection.login(deserialized_info['username'], deserialized_info['password'])
