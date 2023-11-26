import imaplib

class LOGIN():

    # Intialize all the global variables to be used
    def initializeVariables(self,  email, password):
        self.usr = email
        self.pwd = password
        self.mail = None
        self.is_authenticated = False

    # Login to the Gmail account
    def attemptLogin(self):
        try:
            self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            self.mail.login(self.usr, self.pwd)
            print("\nLogin SUCCESSFUL")
            return True
        except Exception as e:
            print("\nLogin FAILED")
            print(f"ERROR: {e}")
            return False         
        
    # Store numerical value of the email  
    def get_authentication(self):
        return self.is_authenticated

    # Store Mail Object
    def get_mail(self):
        return self.mail

    # Function to be executed when the Class has been called
    def __init__(self, email, password):
        # Intialize all the global variables to be used
        self.initializeVariables(email, password)

        # Login to the Gmail account
        self.is_authenticated = self.attemptLogin()

        # Clear data
        self.usr = ''
        self.pwd = ''

        # # Store Mail Object 
        # self.get_mail()

if __name__ == "__main__":
    # Dummy Data
    email = 'senderephishsense@gmail.com'
    password = 'sjbsxjfgyssynixo'

    # Test Login
    run = LOGIN(email, password)
    input = run.get_authentication()

  