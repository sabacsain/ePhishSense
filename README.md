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
        #
                
    # BACK-END
        # Subject as input for searching the email.
        # Multiple Subjects with similar names will cause an error.
            # Quick Fix: Automatically uses the latest email.
        # Persistent Login 
            # Quick Fix: In-memory encryption and saved in a session object.
        # Tested on:
	    # Chrome [WORKING]
	    # Edge [WORKING]
	    # Firefoz [NOT YET TESTED]

    # FRONT-END
        # Connecting HTML files to the back-end
