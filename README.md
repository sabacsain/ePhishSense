# ePhishSense

# REQUIREMENTS
    # Install Flask
        pip install flask

# HOW TO RUN THE APP
    # Go to Google Chrome -> Extensions -> Enable Developer Mode
    # Click Load Unpacked
    # Choose 'flask' folder
        # Make sure that there is no '__pycache__' folder. If so, delete it
    # Execute 'app.py' in vscode
    # Click the ePhishSense extension in browser
    # Enter the email credentials then click Login
    # Enter email subject

# HOW TO UPDATE THE DECISION TREE MODEL
    # Download the latest dataset in csv format
    # a

# ISSUES
    # DATASET
        # Value '111' returns MALICIOUS. It should return SAFE.
        # The decision tree model still only uses 600 emails.
                    
    # BACK-END
        # Subject as input for searching the email.
        # Multiple Subjects with similar names will cause an error.
            # Quick Fix: Automatically uses the latest email.
        # Persistent Login 
            # Quick Fix: Encrypted Login Credentials at runtime or saved in global variable.
        # Currently only tested in chrome browser.

    # FRONT-END
        #
