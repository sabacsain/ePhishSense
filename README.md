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

# ISSUES
    # DATASET
                    
    # BACK-END
        # Subject as input for searching the email.
        # Multiple Subjects with similar names will cause an error.
            # Quick Fix: Automatically uses the latest email.
        # Persistent Login 
            # Quick Fix: Encrypted Login Credentials at runtime or saved in global variable.
        # Currently only tested in chrome browser.

    # FRONT-END
        # Currently have sample GUI
        # Routing of html files
