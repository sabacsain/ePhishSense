import imaplib
import os
import email
import sys
import re
from extension_dt_model import DT_MODEL

# ISSUE/S:
# - CAN'T HANDLE MULTIPLE SIMILAR SUBJECTS

class GMAIL_EXTRACTOR():

    def initializeVariables(self):
        self.usr = ""
        self.pwd = ""
        self.mail = object
        self.mailbox = ""
        self.mailCount = 0
        self.destFolder = ""
        self.data = []
        self.ids = []
        self.idsList = []

        self.valueList = []

    def getLogin(self):
        # print("\nPlease enter your Gmail login details below.")
        # self.usr = input("Email: ")
        # self.pwd = input("Password: ")
        self.usr = 'senderephishsense@gmail.com'
        self.pwd = 'sjbsxjfgyssynixo'

    def attemptLogin(self):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        if self.mail.login(self.usr, self.pwd):
            print("\nLogon SUCCESSFUL")
            return True
        else:
            print("\nLogon FAILED")
            return False

    def checkIfUsersWantsToContinue(self):
        # print(f"\n {self.mailbox}: {self.mailCount} emails")
        return True 
        
    def selectMailbox(self):
        # self.mailbox = input("\nPlease type the name of the mailbox you want to extract, e.g. Inbox: ")
        self.mailbox = 'Inbox'
        bin_count = self.mail.select(self.mailbox)[1]
        self.mailCount = int(bin_count[0].decode("utf-8"))
        return True if self.mailCount > 0 else False

    def searchThroughMailbox(self):
        # type, self.data = self.mail.search(None, "ALL")
        subject = 'SUBJECT "Test with URL"'            # change the SUBJECT as necessary
        type, self.data = self.mail.search(None, subject)
        self.ids = self.data[0]
        self.idsList = self.ids.split()

    def parseEmails(self):
        jsonOutput = {}
        for anEmail in self.data[0].split():
            type, self.data = self.mail.fetch(anEmail, '(UID RFC822)')
            raw = self.data[0][1]
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

            
            # jsonOutput['subject'] = msg['subject']
            # jsonOutput['date'] = msg['date']

            # Get Sender
            jsonOutput['from'] = msg['from']
            # Get DKIM
            jsonOutput['dkim-signature'] = msg['dkim-signature']
            
            raw = self.data[0][0]
            raw_str = raw.decode("utf-8")

            # Get Body 
            if msg.is_multipart():
                for part in msg.walk():
                    partType = part.get_content_type()
                    if partType == "text/html" and "attachment" not in part:
                        jsonOutput['body'] = part.get_payload()
            else:
                jsonOutput['body'] = msg.get_payload(decode=True).decode("utf-8") # Non-multipart email, no attachments or just text.

            print(f"SENDER EMAIL: \n    {jsonOutput['from']}")
            print(f"DKIM: \n    {jsonOutput['dkim-signature']}")
            print(f"BODY: \n     {jsonOutput['body']}")

            def is_url_exists_in_html(html_data):
                # Regular expression to find all URLs in the HTML content
                url_pattern = re.compile(r'href=["\'](https?://\S+?)["\']', re.IGNORECASE)
                urls_exist = url_pattern.findall(html_data)
                
                return True if urls_exist else False
            
            jsonOutput['body'] = is_url_exists_in_html(jsonOutput["body"])

            # Converting Email Data to Numerical Value
            # Sender Email Address
            self.valueList.append(0) if jsonOutput['from'] == 'Null' else self.valueList.append(1)

            # DKIM
            self.valueList.append(0) if jsonOutput['dkim-signature'] == 'Null' else self.valueList.append(1)

            # URL
            self.valueList.append(0) if jsonOutput['body'] == False else self.valueList.append(1)
            
            # print(jsonOutput['from'])
            # print(jsonOutput['dkim-signature'])
            # print(jsonOutput['body'])
            # print(self.valueList)
            # exit(0)
                
    def value(self):
        return self.valueList

    def __init__(self):
        self.initializeVariables()
        self.getLogin()
        if self.attemptLogin():
            not self.selectMailbox() and sys.exit()
        else:
            sys.exit()
        not self.checkIfUsersWantsToContinue() and sys.exit()
        self.searchThroughMailbox()
        self.parseEmails()

if __name__ == "__main__":

    run = GMAIL_EXTRACTOR('', 'sachristopher925@gmail.com', 'sefyrzaynrpilqsm')

    input = run.value()

    predict = DT_MODEL(input)
    prediction = predict.result()
    
    print(input)
    print(prediction)
    