import imaplib

class LOGIN():

    # Intialize all the global variables to be used
    def initializeVariables(self):
        self.usr = ""
        self.pwd = ""
       
        self.value = False

    # Get Gmail credentials
    def getLogin(self, email, password):
        self.usr = email
        self.pwd = password

    # Login to the Gmail account
    def attemptLogin(self):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        if self.mail.login(self.usr, self.pwd):
            print("\nLogin SUCCESSFUL")
            return True
        else:
            print("\nLogin FAILED")
            return False
        
    # Store numerical value of the email  
    def isAuthenticated(self):
        return self.value

    # Function to be executed when the Class has been called
    def __init__(self, email, password):
        # Intialize all the global variables to be used
        self.initializeVariables()

        # Get Gmail credentials
        self.getLogin(email, password)

        # Login to the Gmail account
        self.value = self.attemptLogin()

if __name__ == "__main__":
    # Dummy Data
    email = 'senderephishsense@gmail.com'
    password = 'sjbsxjfgyssynixo'

    # Test Login
    run = LOGIN(email, password)
    input = run.isAuthenticated()

  