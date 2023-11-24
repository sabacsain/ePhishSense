import imaplib, email, re
from extension_dt_model import DT_MODEL


class GMAIL_EXTRACTOR():

    # Intialize all the global variables to be used
    def initializeVariables(self, input_subject, email, password):
        self.subject = input_subject
        self.usr = email
        self.pwd = password
        self.mail = object
        self.mailbox = ""
        self.mailCount = 0
        self.destFolder = ""
        self.data = []
        self.ids = []
        self.idsList = []

        self.valueList = []

    # Get Gmail credentials
    def getLogin(self):
        # print("\nPlease enter your Gmail login details below.")
        # self.usr = input("Email: ")
        # self.pwd = input("Password: ")
        self.usr = self.usr
        self.pwd = self.pwd

    # Login to the Gmail account
    def attemptLogin(self):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        if self.mail.login(self.usr, self.pwd):
            print("\nLogon SUCCESSFUL")
            # Clear data
            self.usr = ''
            self.pwd = ''
            return True
        else:
            print("\nLogon FAILED")
            return False

    # Choose which mailbox to be used
    def selectMailbox(self):
        # self.mailbox = input("\nPlease type the name of the mailbox you want to extract, e.g. Inbox: ")
        self.mailbox = 'Inbox'
        bin_count = self.mail.select(self.mailbox)[1]
        self.mailCount = int(bin_count[0].decode("utf-8"))
        return True if self.mailCount > 0 else False

    def searchThroughMailbox(self):
        # type, self.data = self.mail.search(None, "ALL")
        subject = f'SUBJECT "{self.subject}"'            # change the SUBJECT as necessary
        type, self.data = self.mail.search(None, subject)
        self.ids = self.data[0]
        self.idsList = self.ids.split()

    # Parse Raw Email to get Sender, DKIM, URL
    def parseEmails(self):
        jsonOutput = {}

        type, self.data = self.mail.fetch(self.data[0], '(UID RFC822)')
        raw = self.data[0][1]
       
        # Convert Raw Email to Standard Email Encoding
        try:
            raw_str = raw.decode("utf-8")
        except UnicodeDecodeError:
            try:
                raw_str = raw.decode("ISO-8859-1") # ANSI support
            except UnicodeDecodeError:
                try:
                    raw_str = raw.decode("ascii") # ASCII ?
                except UnicodeDecodeError:
                    pass
                    
        msg = email.message_from_string(raw_str)

        # Get Sender
        jsonOutput['from'] = msg['from']

        # Convert Sender's String Value to Numerical Value
        self.valueList.append(0) if jsonOutput['from'] == 'Null' else self.valueList.append(1)

        # Clear Sender's Value
        print(f"SENDER:\n       {jsonOutput['from']}")
        jsonOutput['from'] = None

        # Get DKIM
        jsonOutput['dkim-signature'] = msg['dkim-signature']

        # Convert DKIM's String Value to Numerical Value
        self.valueList.append(0) if jsonOutput['dkim-signature'] == 'Null' else self.valueList.append(1)

        # Clear DKIM's Value
        print(f"DKIM:\n     {jsonOutput['dkim-signature']}")
        jsonOutput['dkim-signature'] = None
        
        # Get Body 
            # Non-multipart email, no attachments or just text
        if not msg.is_multipart():
            jsonOutput['body'] = msg.get_payload(decode=True).decode("utf-8") 
        else:
            # For Multi-part email.
            for part in msg.walk():
                partType = part.get_content_type()
                if partType == "text/html" and "attachment" not in part:
                    jsonOutput['body'] = part.get_payload()
            
        # print(f"SENDER EMAIL: \n    {jsonOutput['from']}")
        # print(f"DKIM: \n    {jsonOutput['dkim-signature']}")
        # print(f"BODY: \n     {jsonOutput['body']}")

        # Check if URL exists in Body
        def is_url_exists_in_body(html_data):
            # Regular expression to find all URLs in the HTML content
            url_pattern = re.compile(r'href=["\'](https?://\S+?)["\']', re.IGNORECASE)
            # Store all the URLS
            urls_exist = url_pattern.findall(html_data)
            
            return True if urls_exist else False
        
        # Return True or False if URL exists
        jsonOutput['body'] = is_url_exists_in_body(jsonOutput['body'])

        # Convert URL's String Value to Numerical Value
        self.valueList.append(0) if jsonOutput['body'] == False else self.valueList.append(1)

        # Clear URL's Value
        print(f"URL:\n      {jsonOutput['body']}")
        jsonOutput['body'] = None
        
    # Store numerical value of the email  
    def value(self):
        return self.valueList

    # Function to be executed when the Class has been called
    def __init__(self, input_subject, email, password):
        # Intialize all the global variables to be used
        self.initializeVariables(input_subject,email, password)

        # Get Gmail credentials
        self.getLogin()

        # Login to the Gmail account
        if not self.attemptLogin(): exit(0)

        # Select which Mailbox to be used
        self.selectMailbox()

        # Search the email to be scanned
        self.searchThroughMailbox()

        # Extract Sender, DKIM, and URL
        self.parseEmails()

if __name__ == "__main__":
    run = GMAIL_EXTRACTOR('Random', 'senderephishsense@gmail.com', 'sjbsxjfgyssynixo')
    input = run.value()

    predict = DT_MODEL(input)
    prediction = predict.result()
    
    print(f"Numerical Value: {input}")
    print(f"Result: {prediction}")
    