import email, re, csv, os, platform
from extension_dt_model import DT_MODEL
import imaplib


class GMAIL_EXTRACTOR():

    # Intialize all the global variables to be used
    def initializeVariables(self, input_subject, mail):
        self.subject = input_subject
        self.usr = ""
        self.pwd = ""
        self.mail = mail
        self.mailbox = ""
        self.mailCount = 0
        self.destFolder = ""
        self.data = []
        self.ids = []
        self.idsList = []

        self.valueList = []
        self.is_subject_found = True

    # # Get Gmail credentials
    # def getLogin(self):
    #     # print("\nPlease enter your Gmail login details below.")
    #     # self.usr = input("Email: ")
    #     # self.pwd = input("Password: ")
    #     self.usr = 'senderephishsense@gmail.com'
    #     self.pwd = 'sjbsxjfgyssynixo'

    # # Login to the Gmail account
    # def attemptLogin(self):
    #     self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    #     if self.mail.login(self.usr, self.pwd):
    #         print("\nLogon SUCCESSFUL")
    #         return True
    #     else:
    #         print("\nLogon FAILED")
    #         return False
        
    # Choose which mailbox to be used
    def selectMailbox(self):
        self.mailbox = 'Inbox'
        bin_count = self.mail.select(self.mailbox)[1]
        self.mailCount = int(bin_count[0].decode("utf-8"))
        return True if self.mailCount > 0 else False

    def searchThroughMailbox(self):

        # type, self.data = self.mail.search(None, "ALL")
        subject = f'SUBJECT "{self.subject}"'         
        type, self.data = self.mail.search(None, subject)
     
        # Check if no subject matches
        if not type == 'OK' or not self.data[0]:
            print('EMPTY')
            return False

        self.ids = self.data[0]
        self.idsList = self.ids.split()

        # NOTE: UNCOMMENT IF THERE IS A WAY FOR MORE THAN TWO EMAIL SUBJ.
        # Check if subjects are more than 1
        # if len(self.idsList) > 1:
        #     print('subject more thatn 1')
        #     # DO SOMETHING
        #     # return True

        #     # FOR TESTING PURPOSES
        #     raise Exception
        #     return False
        return True      

    # Parse Raw Email to get Sender, DKIM, URL
    def parseEmails(self):
        jsonOutput = {}

        type, self.data = self.mail.fetch(self.idsList[-1], '(UID RFC822)')
        raw = self.data[0][1]

        # Convert Raw Email to Standard Email Encoding
        try:
            raw_str = raw.decode("utf-8")
        except UnicodeDecodeError as utf_err:
            try:
                raw_str = raw.decode("ISO-8859-1") # ANSI support
            except UnicodeDecodeError as iso_err:
                try:
                    raw_str = raw.decode("ascii") # ASCII ?
                except UnicodeDecodeError as ascii_err:
                    print(f"Error decoding as UTF-8: {utf_err}")
                    print(f"Error decoding as ISO-8859-1: {iso_err}")
                    print(f"Error decoding as ASCII: {ascii_err}")
          
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
            

        # Check if URL exists in Body
        def is_url_exists_in_body(html_data):
            # Get the OS 
            which_os = platform.system()

            # Perform forward/backward slash depending on the OS
            slash = '\\' if which_os == 'Windows' else '/'

            # Get the current directory
            current_path = os.path.dirname(os.path.abspath(__file__))

            # Concatenate directory path and dataset location
            filepath = current_path + slash + 'blacklisted_urls.csv'

            # Open the CSV file and read its content
            with open(filepath, 'r') as csv_file:
                # Use the csv.reader to read the file
                csv_reader = csv.reader(csv_file)

                # Skip the header
                next(csv_reader, None)

                # Store only the URLs column and saved it as a list
                blacklist = [row[0].lower() for row in csv_reader]

            # Regular expression to find all URLs in the HTML content
            url_pattern = re.compile(r'(https?://\S+)', re.IGNORECASE)
            # Store all the URLS
            urls_exist = url_pattern.findall(html_data)

            if not urls_exist:
                return None # No URLs Found

            for url in urls_exist:
                if any(blacklisted_url.lower() in url.lower() for blacklisted_url in blacklist):
                    return True # Blacklisted URL matches

            return False # No Blacklisted URL matches
        
        # Return True or False if URL exists
        jsonOutput['body'] = is_url_exists_in_body(jsonOutput['body'])

        # Convert URL's String Value to Numerical Value
        if jsonOutput['body'] is True:
            self.valueList.append(-1) # if url found as blacklisted
        elif jsonOutput['body'] is False:
            self.valueList.append(1) # if url found as not in the list of blacklisted
        elif jsonOutput['body'] is None:
            self.valueList.append(0) # if there's no url found
        #self.valueList.append(jsonOutput['body'])

        # Clear URL's Value
        print(f"URL:\n      {jsonOutput['body']}")
        jsonOutput['body'] = None
        
    # Store numerical value of the email  
    def value(self):
        return self.valueList

    # Get mailbox value
    def get_is_subject_found(self):
        return self.is_subject_found

    # Function to be executed when the Class has been called
    def __init__(self, input_subject, mail):
        # Intialize all the global variables to be used
        self.initializeVariables(input_subject, mail)

        ## Get Gmail credentials
        # self.getLogin()

        ## Login to the Gmail account
        # if not self.attemptLogin(): exit(0)

        # Select which Mailbox to be used
        self.selectMailbox()

        # Search the email to be scanned
        if not self.searchThroughMailbox():
            self.is_subject_found = False
            print('Subject not found')
            return 

        # Extract Sender, DKIM, and URL
        self.parseEmails()

if __name__ == "__main__":
    run = GMAIL_EXTRACTOR('Random','mail')
    input = run.value()

    predict = DT_MODEL(input)
    prediction = predict.result()
    
    print(f"Numerical Value: {input}")
    print(f"Result: {prediction}")
    